def quick_sort(candidates):
    if len(candidates) <= 1:
        return candidates
    pivot = candidates[0]
    left = [x for x in candidates[1:] if x["score"] >= pivot["score"]]
    right = [x for x in candidates[1:] if x["score"] < pivot["score"]]
    return quick_sort(left) + [pivot] + quick_sort(right)

def greedy_select(candidates, job_skills, k=5):
    shortlist = []
    for c in candidates:
        matches = sum([1 for s in job_skills if s.lower() in c["skills"].lower()])
        if matches > 0:
            shortlist.append(c)
        if len(shortlist) >= k:
            break
    return shortlist
