# frozen_string_literal: true

require 'spec_helper'

RSpec.describe LarpMyResumeReport::Renderer do
  describe '.color_class' do
    it 'returns score-green for >= 70' do
      expect(described_class.color_class(70)).to eq('score-green')
      expect(described_class.color_class(100)).to eq('score-green')
    end

    it 'returns score-yellow for 50-69' do
      expect(described_class.color_class(50)).to eq('score-yellow')
      expect(described_class.color_class(69)).to eq('score-yellow')
    end

    it 'returns score-red for < 50' do
      expect(described_class.color_class(0)).to eq('score-red')
      expect(described_class.color_class(49)).to eq('score-red')
    end

    it 'returns score-unknown for nil' do
      expect(described_class.color_class(nil)).to eq('score-unknown')
    end
  end

  describe '.render' do
    let(:full_match_data) { JSON.parse(File.read(File.join(__dir__, 'fixtures', 'full_match.json'))) }
    let(:scan_only_data)  { JSON.parse(File.read(File.join(__dir__, 'fixtures', 'scan_only.json'))) }

    it 'renders a non-empty HTML string' do
      html = described_class.render(full_match_data)
      expect(html).to be_a(String)
      expect(html).not_to be_empty
      expect(html.downcase).to include('<html')
    end

    it 'contains no external script or stylesheet references (RUBY-04)' do
      html = described_class.render(full_match_data)
      expect(html).not_to include('src="http')
      expect(html).not_to include("src='http")
      expect(html).not_to include('href="http')
      expect(html).not_to include("href='http")
    end

    it 'includes SVG bar chart when keyword_match is present (RUBY-06)' do
      html = described_class.render(full_match_data)
      expect(html).to include('<svg')
      expect(html).to include('<rect')
    end

    it 'omits SVG bar chart when keyword_match is null (RUBY-06 + D-03)' do
      html = described_class.render(scan_only_data)
      expect(html).not_to include('<svg')
      expect(html).not_to include('<rect')
    end

    it 'shows keyword analysis placeholder when keyword_match is null' do
      html = described_class.render(scan_only_data)
      expect(html).to include('larp-my-resume match')
    end

    it 'includes the score color class in the score hero section (RUBY-05)' do
      html = described_class.render(full_match_data)
      expect(html).to match(/score-green|score-yellow|score-red/)
    end

    it 'displays the overall_score value (72) from the fixture (RUBY-05)' do
      html = described_class.render(full_match_data)
      expect(html).to include('72')
    end

    it 'includes bullet text from the bullets array (D-09)' do
      html = described_class.render(full_match_data)
      expect(html).to include('Built a distributed system')
    end

    it 'includes ATS flag name from ats_flags array (D-10)' do
      html = described_class.render(scan_only_data)
      # flag name may be HTML-escaped — check for key substring
      expect(html).to include('non_standard_heading')
    end

    it 'renders overall_score as N/A when score is nil' do
      data = JSON.parse(full_match_data.to_json)
      data['score_breakdown'] = nil
      data['overall_score'] = nil
      html = described_class.render(data)
      expect(html).to include('N/A')
    end
  end
end
