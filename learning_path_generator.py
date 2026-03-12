from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class LearningModule:
    name: str
    level: str
    estimated_hours: int
    outcome: str


SKILL_GAPS = {
    "python": [
        LearningModule("Python Fundamentals", "beginner", 12, "Write scripts with functions and data structures"),
        LearningModule("Intermediate Python", "intermediate", 14, "Build modular applications using OOP and testing"),
    ],
    "sql": [
        LearningModule("SQL Basics", "beginner", 10, "Query relational data with SELECT and JOIN"),
        LearningModule("Advanced SQL", "intermediate", 12, "Design optimized analytical queries"),
    ],
    "machine learning": [
        LearningModule("ML Foundations", "beginner", 16, "Understand supervised and unsupervised workflows"),
        LearningModule("Applied Machine Learning", "intermediate", 18, "Train and evaluate end-to-end models"),
    ],
    "system design": [
        LearningModule("Scalable System Design", "intermediate", 20, "Design resilient distributed services"),
    ],
    "react": [
        LearningModule("React Fundamentals", "beginner", 12, "Build reusable UI components with state"),
    ],
    "docker": [
        LearningModule("Docker for Developers", "beginner", 8, "Containerize applications for consistent deployment"),
    ],
}

GOAL_PRIORITIES = {
    "become data scientist": ["python", "sql", "machine learning"],
    "become ml engineer": ["python", "machine learning", "docker", "system design"],
    "become full stack developer": ["python", "react", "sql", "docker"],
}


class LearningPathGenerator:
    def __init__(self, goals: Iterable[str], current_skills: Iterable[str], recommended_technologies: Iterable[str]) -> None:
        self.goals = [g.strip().lower() for g in goals if g.strip()]
        self.current_skills = {s.strip().lower() for s in current_skills if s.strip()}
        self.recommended_technologies = [t.strip().lower() for t in recommended_technologies if t.strip()]

    def generate(self) -> dict:
        priorities = self._derive_priorities()
        modules = self._create_modules(priorities)
        milestones = self._build_milestones(modules)

        return {
            "goals": self.goals,
            "current_skills": sorted(self.current_skills),
            "recommended_technologies": self.recommended_technologies,
            "learning_modules": [m.__dict__ for m in modules],
            "milestones": milestones,
            "total_estimated_hours": sum(module.estimated_hours for module in modules),
        }

    def _derive_priorities(self) -> list[str]:
        ranked: list[str] = []

        for goal in self.goals:
            ranked.extend(GOAL_PRIORITIES.get(goal, []))

        ranked.extend(self.recommended_technologies)

        if not ranked:
            ranked = ["python", "sql", "machine learning"]

        seen = set()
        deduped = []
        for item in ranked:
            if item not in seen:
                seen.add(item)
                deduped.append(item)

        return deduped

    def _create_modules(self, priorities: Iterable[str]) -> list[LearningModule]:
        modules: list[LearningModule] = []

        for skill in priorities:
            if skill in self.current_skills:
                continue
            skill_modules = SKILL_GAPS.get(skill)
            if not skill_modules:
                modules.append(
                    LearningModule(
                        name=f"{skill.title()} Essentials",
                        level="beginner",
                        estimated_hours=10,
                        outcome=f"Demonstrate practical competency in {skill}",
                    )
                )
            else:
                modules.extend(skill_modules)

        if not modules:
            modules.append(
                LearningModule(
                    name="Capstone Project",
                    level="advanced",
                    estimated_hours=20,
                    outcome="Build a portfolio-ready project aligned to your goals",
                )
            )

        return modules

    def _build_milestones(self, modules: list[LearningModule]) -> list[dict]:
        milestones = []
        cumulative = 0
        for index, module in enumerate(modules, start=1):
            cumulative += module.estimated_hours
            milestones.append(
                {
                    "milestone": f"Week {index}",
                    "focus": module.name,
                    "target_hours": module.estimated_hours,
                    "cumulative_hours": cumulative,
                }
            )
        return milestones


def parse_csv(value: str) -> list[str]:
    return [item.strip() for item in value.split(",") if item.strip()]


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate a personalized learning path using goals, existing skills, and recommended technologies."
    )
    parser.add_argument("--goals", default="", help="Comma-separated goals. Example: 'become data scientist'")
    parser.add_argument("--skills", default="", help="Comma-separated current skills. Example: 'python,sql'")
    parser.add_argument(
        "--tech",
        default="",
        help="Comma-separated recommended technologies. Example: 'docker,airflow'",
    )

    args = parser.parse_args()

    generator = LearningPathGenerator(
        goals=parse_csv(args.goals),
        current_skills=parse_csv(args.skills),
        recommended_technologies=parse_csv(args.tech),
    )
    print(json.dumps(generator.generate(), indent=2))


if __name__ == "__main__":
    main()
