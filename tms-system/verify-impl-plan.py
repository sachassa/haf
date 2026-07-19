#!/usr/bin/env python3
import json
import sys

with open('impl-plan.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

tasks = data['tasks']
task_ids = {t['id'] for t in tasks}
errors = []

# 1. DAG 사이클 검증
def detect_cycle(task_id, visited, rec_stack, dep_map):
    visited.add(task_id)
    rec_stack.add(task_id)

    for dep in dep_map.get(task_id, []):
        if dep not in visited:
            if detect_cycle(dep, visited, rec_stack, dep_map):
                return True
        elif dep in rec_stack:
            return True

    rec_stack.remove(task_id)
    return False

dep_map = {t['id']: t.get('dependsOn', []) for t in tasks}
visited = set()
for tid in task_ids:
    if tid not in visited:
        if detect_cycle(tid, visited, set(), dep_map):
            errors.append(f"DAG cycle detected: {tid}")

# 2. dependsOn reference validity
for t in tasks:
    for dep in t.get('dependsOn', []):
        if dep not in task_ids:
            errors.append(f"Task '{t['id']}' dependsOn references non-existent task: {dep}")

# 3. ownedBoundary non-nesting
def is_ancestor(path1, path2):
    p1_parts = path1.rstrip('/\\').split('/')
    p2_parts = path2.rstrip('/\\').split('/')
    return len(p1_parts) <= len(p2_parts) and p2_parts[:len(p1_parts)] == p1_parts

boundaries = {}
for t in tasks:
    boundaries[t['id']] = t.get('ownedBoundary', [])

for t1_id, paths1 in boundaries.items():
    for t2_id, paths2 in boundaries.items():
        if t1_id >= t2_id:
            continue
        for p1 in paths1:
            for p2 in paths2:
                if is_ancestor(p1, p2) or is_ancestor(p2, p1):
                    errors.append(f"ownedBoundary nesting violation: '{p1}' <-> '{p2}' in tasks '{t1_id}', '{t2_id}'")

# 4. Milestone placement
milestones = [t for t in tasks if t['unitType'] == 'milestone']
implementations = [t for t in tasks if t['unitType'] == 'implementation']

if len(milestones) != 1:
    errors.append(f"Expected 1 milestone, got {len(milestones)}")
else:
    milestone = milestones[0]
    if not milestone.get('ownedBoundary'):
        errors.append(f"Milestone '{milestone['id']}' has empty ownedBoundary")

# 5. Field lengths
for t in tasks:
    task_field = t.get('task', '')
    done_field = t.get('done', '')

    if len(task_field) < 50:
        errors.append(f"Task '{t['id']}' task field too short")
    if len(done_field) < 20:
        errors.append(f"Task '{t['id']}' done field too short")

# 6. Protected boundary not in ownedBoundary
protected_prefixes = ['.claude', 'docs/solution-design.md']
for t in tasks:
    for boundary in t.get('ownedBoundary', []):
        for protected in protected_prefixes:
            if boundary.startswith(protected):
                errors.append(f"Task '{t['id']}' ownedBoundary includes protected: {boundary}")

if errors:
    print("FAILURES:")
    for err in errors:
        print(f"  {err}")
    sys.exit(1)
else:
    print("✓ DAG cycles: none")
    print("✓ dependsOn references: valid")
    print("✓ ownedBoundary non-nesting: confirmed")
    print("✓ milestone placement: correct")
    print("✓ task/done fields: adequate")
    print("✓ protected boundaries: not violated")
    print("\nDEEP VALIDATION PASSED")
    sys.exit(0)
