# frozen_string_literal: true

require 'spec_helper'
require 'json'

RSpec.describe LarpMyResumeReport::Parser do
  let(:fixtures_dir) { File.join(__dir__, 'fixtures') }

  describe '.parse' do
    context 'with a valid full-match fixture (schema_version 1.0)' do
      let(:raw) { File.read(File.join(fixtures_dir, 'full_match.json')) }

      it 'returns a Hash' do
        expect(described_class.parse(raw)).to be_a(Hash)
      end

      it 'has schema_version 1.0' do
        expect(described_class.parse(raw)['schema_version']).to eq('1.0')
      end

      it 'has overall_score as an Integer' do
        expect(described_class.parse(raw)['overall_score']).to be_an(Integer)
      end

      it 'has keyword_match as a Hash (not nil)' do
        expect(described_class.parse(raw)['keyword_match']).to be_a(Hash)
      end
    end

    context 'with a scan-only fixture (keyword_match null)' do
      let(:raw) { File.read(File.join(fixtures_dir, 'scan_only.json')) }

      it 'returns a Hash' do
        expect(described_class.parse(raw)).to be_a(Hash)
      end

      it 'has keyword_match as nil' do
        expect(described_class.parse(raw)['keyword_match']).to be_nil
      end

      it 'has score_breakdown.keyword_score as nil' do
        expect(described_class.parse(raw).dig('score_breakdown', 'keyword_score')).to be_nil
      end
    end

    context 'with bad schema_version (2.0)' do
      let(:raw) { File.read(File.join(fixtures_dir, 'bad_version.json')) }

      it 'exits with status 1' do
        expect { described_class.parse(raw) }.to raise_error(SystemExit) do |e|
          expect(e.status).to eq(1)
        end
      end
    end

    context 'with valid JSON whose root is not a Hash' do
      it 'exits with status 1 when root is an array' do
        expect { described_class.parse('[]') }.to raise_error(SystemExit) do |e|
          expect(e.status).to eq(1)
        end
      end

      it 'exits with status 1 when root is a number' do
        expect { described_class.parse('42') }.to raise_error(SystemExit) do |e|
          expect(e.status).to eq(1)
        end
      end

      it 'exits with status 1 when root is a string' do
        expect { described_class.parse('"hello"') }.to raise_error(SystemExit) do |e|
          expect(e.status).to eq(1)
        end
      end
    end

    context 'with malformed JSON' do
      it 'exits with status 1 on empty string' do
        expect { described_class.parse('') }.to raise_error(SystemExit) do |e|
          expect(e.status).to eq(1)
        end
      end

      it 'exits with status 1 on non-JSON string' do
        expect { described_class.parse('not json at all') }.to raise_error(SystemExit) do |e|
          expect(e.status).to eq(1)
        end
      end

      it 'exits with status 1 on truncated JSON' do
        expect { described_class.parse('{"schema_version": "1.0"') }.to raise_error(SystemExit) do |e|
          expect(e.status).to eq(1)
        end
      end
    end
  end
end
