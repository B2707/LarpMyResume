# frozen_string_literal: true

require 'json'

module LarpMyResumeReport
  module Parser
    SUPPORTED_VERSION_RE = /\A1\.\d/.freeze

    def self.parse(raw)
      begin
        data = JSON.parse(raw)
      rescue JSON::ParserError => e
        warn "Error: invalid JSON — #{e.message}"
        exit 1
      end

      unless data.is_a?(Hash)
        warn "Error: JSON root must be an object, got #{data.class.name.downcase}."
        exit 1
      end

      version = data["schema_version"].to_s
      unless SUPPORTED_VERSION_RE.match?(version)
        warn "Error: schema_version '#{version}' not supported. Expected 1.x."
        exit 1
      end
      data
    end
  end
end
