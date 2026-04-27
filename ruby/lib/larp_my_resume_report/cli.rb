# frozen_string_literal: true

require 'optparse'
require_relative 'parser'
require_relative 'renderer'

module LarpMyResumeReport
  module CLI
    def self.run(argv)
      options = {}

      opt_parser = OptionParser.new do |opts|
        opts.banner = "Usage: larp-my-resume-report [--out FILE] [--file JSON_FILE]"
        opts.on("--file FILE", "Read JSON from FILE (default: stdin)")      { |v| options[:file] = v }
        opts.on("--out FILE",  "Write HTML to FILE (default: stdout)")      { |v| options[:out] = v }
        opts.on("-h", "--help", "Show this help") { puts opts; exit 0 }
      end

      begin
        opt_parser.parse!(argv)
      rescue OptionParser::InvalidOption => e
        warn "Error: #{e.message}"
        warn opt_parser.to_s
        exit 1
      end

      # RUBY-02: no hang on bare invocation — check tty BEFORE set_encoding (Pitfall 2+3)
      if $stdin.tty? && options[:file].nil?
        puts opt_parser
        exit 0
      end

      # Set encoding BEFORE reading (Pitfall 3: must precede $stdin.read)
      $stdin.set_encoding("UTF-8") unless options[:file]
      begin
        raw = options[:file] ? File.read(options[:file], encoding: 'UTF-8') : $stdin.read
      rescue Errno::ENOENT, Errno::EACCES => e
        warn "Error: cannot read input file — #{e.message}"
        exit 1
      end

      data = LarpMyResumeReport::Parser.parse(raw)
      html = LarpMyResumeReport::Renderer.render(data)

      if options[:out]
        begin
          File.write(options[:out], html, encoding: 'UTF-8')
        rescue Errno::ENOENT, Errno::EACCES => e
          warn "Error: cannot write output file — #{e.message}"
          exit 1
        end
      else
        $stdout.write(html)
      end
    end
  end
end
