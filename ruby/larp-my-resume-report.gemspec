# frozen_string_literal: true

Gem::Specification.new do |spec|
  spec.name          = "larp-my-resume-report"
  spec.version       = "0.1.0"
  spec.authors       = ["Bader Asadi"]
  spec.email         = ["baderasadi07@gmail.com"]
  spec.summary       = "HTML report generator for larp-my-resume JSON output"
  spec.description   = "Reads larp-my-resume --json output and renders a self-contained HTML report."
  spec.homepage      = "https://github.com/B2707/LarpMyResume"
  spec.license       = "MIT"

  spec.required_ruby_version = ">= 3.0"

  # CRITICAL: lib/**/*.erb must be included or template is missing after gem install
  spec.files         = Dir["lib/**/*.rb"] + Dir["lib/**/*.erb"] + Dir["bin/*"]
  spec.bindir        = "bin"
  spec.executables   = ["larp-my-resume-report"]
  spec.require_paths = ["lib"]

  # Dev only — zero runtime dependencies
  spec.add_development_dependency "rspec", "~> 3.13"
  spec.add_development_dependency "rake"
end
