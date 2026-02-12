def calculate_match(candidate_skills, job_skills):
    candidate_set = {
        skill.strip().lower()
        for skill in candidate_skills.split(',')
        if skill.strip()
    }

    job_set = {
        skill.strip().lower()
        for skill in job_skills.split(',')
        if skill.strip()
    }

    if not job_set:
        return 0

    matched = candidate_set.intersection(job_set)
    return int((len(matched) / len(job_set)) * 100)
