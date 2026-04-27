# frozen_string_literal: true

require 'json'

# Add lib to load path for in-repo development (before gem is installed)
$LOAD_PATH.unshift(File.join(File.dirname(__FILE__), '..', 'lib'))

require 'larp_my_resume_report/parser'
require 'larp_my_resume_report/renderer'

RSpec.configure do |config|
  config.order = :random
  config.expect_with :rspec do |expectations|
    expectations.syntax = :expect  # expect syntax only — not should
  end
end
