"""Skills gazetteer — canonical skill names, aliases, parent/child hierarchy."""
from __future__ import annotations

# canonical_name -> list[aliases]  (first alias is the display name)
# Minimum 60 entries covering SE candidates 2025: languages, frameworks,
# databases, infra/cloud, tools, protocols.
#
# Rule: each entry's alias list must contain the canonical key (or a string
# containing it as a substring) so that `test_gazetteer_canonical_has_alias`
# passes. The canonical key is the lowercase identifier; at least one alias
# should include it (e.g. lowercase variant) for the self-reference check.
GAZETTEER: dict[str, list[str]] = {
    # ── Languages ──
    "python":       ["Python", "python"],
    "javascript":   ["JavaScript", "javascript", "js"],
    "typescript":   ["TypeScript", "typescript", "ts"],
    "go":           ["Go", "golang"],
    "rust":         ["Rust", "rust-lang"],
    "java":         ["Java", "java"],
    "cpp":          ["C++", "cpp", "c plus plus"],
    "csharp":       ["C#", "csharp", ".NET", "dotnet"],
    "ruby":         ["Ruby", "ruby"],
    "swift":        ["Swift", "swift"],
    "kotlin":       ["Kotlin", "kotlin"],
    "scala":        ["Scala", "scala"],
    "r":            ["r"],
    "c":            ["c"],
    "php":          ["PHP", "php"],
    "bash":         ["Bash", "bash", "shell", "sh"],
    # ── Frontend Frameworks ──
    "react":        ["React", "react", "reactjs", "react.js"],
    "vue":          ["Vue", "vue", "vuejs", "vue.js"],
    "angular":      ["Angular", "angular", "angularjs"],
    "nextjs":       ["Next.js", "nextjs"],
    "svelte":       ["Svelte", "svelte"],
    # ── Backend Frameworks ──
    "django":       ["Django", "django"],
    "fastapi":      ["FastAPI", "fastapi"],
    "flask":        ["Flask", "flask"],
    "express":      ["Express", "express", "expressjs", "express.js"],
    "spring":       ["Spring", "spring", "Spring Boot", "springboot"],
    "rails":        ["Rails", "rails", "Ruby on Rails"],
    "laravel":      ["Laravel", "laravel"],
    "nodejs":       ["Node.js", "nodejs", "node"],
    # ── Databases (SQL) ──
    "sql":          ["SQL", "sql"],
    "postgresql":   ["PostgreSQL", "postgresql", "postgres"],
    "mysql":        ["MySQL", "mysql"],
    "sqlite":       ["SQLite", "sqlite"],
    "mssql":        ["SQL Server", "mssql", "microsoft sql server"],
    # ── Databases (NoSQL) ──
    "mongodb":      ["MongoDB", "mongodb", "mongo"],
    "redis":        ["Redis", "redis"],
    "elasticsearch": ["Elasticsearch", "elasticsearch", "elastic", "opensearch"],
    "dynamodb":     ["DynamoDB", "dynamodb"],
    "cassandra":    ["Cassandra", "cassandra"],
    # ── Cloud / Infra ──
    "aws":          ["AWS", "aws", "amazon web services"],
    "gcp":          ["GCP", "gcp", "google cloud", "google cloud platform"],
    "azure":        ["Azure", "azure", "microsoft azure"],
    "docker":       ["Docker", "docker"],
    "kubernetes":   ["Kubernetes", "kubernetes", "k8s"],
    "terraform":    ["Terraform", "terraform"],
    "ansible":      ["Ansible", "ansible"],
    "linux":        ["Linux", "linux", "unix"],
    "nginx":        ["Nginx", "nginx"],
    # ── CI/CD + DevOps ──
    "git":          ["Git", "git"],
    "github_actions": ["GitHub Actions", "github_actions"],
    "jenkins":      ["Jenkins", "jenkins"],
    "cicd":         ["CI/CD", "cicd", "ci cd", "continuous integration", "continuous delivery"],
    # ── Data / ML ──
    "pandas":       ["pandas"],
    "numpy":        ["numpy"],
    "pytorch":      ["PyTorch", "pytorch"],
    "tensorflow":   ["TensorFlow", "tensorflow"],
    "spark":        ["Spark", "spark", "apache spark"],
    # ── Protocols / APIs ──
    "rest":         ["REST", "rest", "rest api", "rest apis", "restful"],
    "graphql":      ["GraphQL", "graphql"],
    "grpc":         ["gRPC", "grpc"],
    "kafka":        ["Kafka", "kafka", "apache kafka"],
    "rabbitmq":     ["RabbitMQ", "rabbitmq"],
    # ── Tools ──
    "celery":       ["Celery", "celery"],
    "pytest":       ["pytest"],
    "jest":         ["Jest", "jest"],
    "webpack":      ["Webpack", "webpack"],
    "vite":         ["Vite", "vite"],
    "figma":        ["Figma", "figma"],
    "jira":         ["Jira", "jira"],
}

# child → parent: resume child weakly satisfies JD parent (one-directional only)
SKILL_PARENTS: dict[str, str] = {
    # SQL children
    "postgresql": "sql",
    "mysql":      "sql",
    "sqlite":     "sql",
    "mssql":      "sql",
    # JavaScript children
    "react":      "javascript",
    "vue":        "javascript",
    "angular":    "javascript",
    "express":    "javascript",
    "nextjs":     "javascript",
    "nodejs":     "javascript",
    "svelte":     "javascript",
    # Python children
    "pandas":     "python",
    "numpy":      "python",
    "django":     "python",
    "fastapi":    "python",
    "flask":      "python",
    # Java children
    "spring":     "java",
    # Ruby children
    "rails":      "ruby",
    # Docker parent for k8s
    "kubernetes": "docker",
    # CI/CD umbrella
    "github_actions": "cicd",
    "jenkins":    "cicd",
}

# Short/ambiguous terms that require comma-list context or alias match
DISAMBIGUATION_BLOCKLIST: frozenset[str] = frozenset({
    "go", "r", "c", "swift", "rust", "scala",
})
