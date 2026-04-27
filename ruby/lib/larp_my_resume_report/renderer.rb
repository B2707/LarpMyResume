# frozen_string_literal: true

require 'erb'

module LarpMyResumeReport
  module Renderer
    TEMPLATE_PATH = File.join(File.dirname(__FILE__), 'templates', 'report.html.erb').freeze

    # Color thresholds — mirror Python cli.py lines exactly (RUBY-05)
    # green >= 70, yellow 50-69, red < 50
    def self.color_class(score)
      return "score-unknown" if score.nil?

      if    score >= 70 then "score-green"
      elsif score >= 50 then "score-yellow"
      else                   "score-red"
      end
    end

    def self.render(data)
      template = File.read(TEMPLATE_PATH, encoding: 'UTF-8')
      erb = ERB.new(template, trim_mode: '-')

      overall_score   = data.dig("score_breakdown", "overall_score") || data["overall_score"]
      score_color     = color_class(overall_score)
      keyword_match   = data["keyword_match"]   # nil for scan-only
      bullets         = data["bullets"] || []
      ats_flags       = data["ats_flags"] || []
      score_breakdown = data["score_breakdown"]

      hits_count = keyword_match ? (keyword_match["hits"]    || []).length : 0
      weak_count = keyword_match ? (keyword_match["weak"]    || []).length : 0
      miss_count = keyword_match ? (keyword_match["missing"] || []).length : 0
      max_count  = [hits_count, weak_count, miss_count, 1].max  # 1 prevents div-by-zero
      bar_scale  = 200.0 / max_count

      erb.result_with_hash(
        overall_score:   overall_score,
        score_color:     score_color,
        score_breakdown: score_breakdown,
        keyword_match:   keyword_match,
        hits_count:      hits_count,
        weak_count:      weak_count,
        miss_count:      miss_count,
        bar_scale:       bar_scale,
        bullets:         bullets,
        ats_flags:       ats_flags,
        resume_file:     data["resume_file"],
        generated_at:    data["generated_at"],
      )
    end
  end
end
