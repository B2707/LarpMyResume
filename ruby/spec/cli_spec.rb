# frozen_string_literal: true

require 'spec_helper'
require 'larp_my_resume_report/cli'
require 'tmpdir'

RSpec.describe LarpMyResumeReport::CLI do
  let(:fixtures_dir) { File.join(__dir__, 'fixtures') }
  let(:scan_only_fixture) { File.join(fixtures_dir, 'scan_only.json') }

  describe '.run' do
    # TTY guard: when stdin is a tty and no --file is given, print help and exit 0
    context 'when invoked bare (tty stdin, no --file)' do
      it 'exits with status 0 instead of hanging' do
        # Stub $stdin.tty? to return true so the guard triggers cleanly
        allow($stdin).to receive(:tty?).and_return(true)
        # No --file, no --out — bare invocation
        expect { described_class.run([]) }.to raise_error(SystemExit) do |e|
          expect(e.status).to eq(0)
        end
      end
    end

    # Happy path: --file points to a valid fixture, --out is a writable path
    context 'with --file pointing to a valid fixture and a writable --out path' do
      it 'writes an HTML report and exits cleanly' do
        Dir.mktmpdir do |tmpdir|
          out_path = File.join(tmpdir, 'report.html')
          described_class.run(['--file', scan_only_fixture, '--out', out_path])
          expect(File.exist?(out_path)).to be true
          content = File.read(out_path, encoding: 'UTF-8')
          expect(content.downcase).to include('<html')
        end
      end
    end

    # Missing --file: expect clean error message and exit 1
    context 'with --file pointing to a nonexistent path' do
      it 'exits with status 1' do
        Dir.mktmpdir do |tmpdir|
          out_path = File.join(tmpdir, 'report.html')
          expect do
            described_class.run(['--file', '/nonexistent_fixture_12345.json', '--out', out_path])
          end.to raise_error(SystemExit) do |e|
            expect(e.status).to eq(1)
          end
        end
      end
    end

    # Bad --out directory: output directory does not exist
    context 'with --out pointing to a nonexistent directory' do
      it 'exits with status 1' do
        expect do
          described_class.run(['--file', scan_only_fixture, '--out', '/nonexistent_dir_12345/report.html'])
        end.to raise_error(SystemExit) do |e|
          expect(e.status).to eq(1)
        end
      end
    end

    # RUBY-01: when --out is omitted, write HTML to $stdout (not an error)
    context 'when --out is not provided' do
      it 'writes HTML to stdout and exits cleanly' do
        captured = StringIO.new
        allow($stdout).to receive(:write) { |str| captured.write(str) }
        described_class.run(['--file', scan_only_fixture])
        expect(captured.string.downcase).to include('<html')
      end
    end

    # Unknown flag: OptionParser::InvalidOption should be rescued cleanly
    context 'with an unrecognized flag' do
      it 'exits with status 1 instead of raising unhandled OptionParser::InvalidOption' do
        expect do
          described_class.run(['--verbose'])
        end.to raise_error(SystemExit) do |e|
          expect(e.status).to eq(1)
        end
      end
    end
  end
end
