# frozen_string_literal: true

require "json"
require "kramdown"

module Kramdown
  module Converter
    module MathEngine
      # Converts kramdown math elements ($$...$$) to MathML at build time using temml.
      module Mathml
        WORKER_PATH = File.expand_path("mathml-worker.js", __dir__)
        MUTEX = Mutex.new

        def self.call(_converter, el, opts)
          display_mode = el.options[:category] == :block
          html = render(el.value, display_mode)

          if display_mode
            "#{' ' * opts}#{html}\n"
          else
            html
          end
        end

        def self.render(tex, display_mode)
          MUTEX.synchronize do
            request = JSON.generate({ tex: tex, displayMode: display_mode })
            2.times do
              io = ensure_worker
              begin
                io.puts(request)
                io.flush
                line = io.gets
                raise IOError, "mathml-worker closed stdout" if line.nil?

                response = JSON.parse(line)
                raise RuntimeError, response["error"] if response["error"]

                return response.fetch("html")
              rescue IOError, Errno::EPIPE
                reset_worker
              end
            end

            raise RuntimeError, "mathml-worker failed after retry"
          end
        end

        def self.ensure_worker
          return @worker if @worker && !@worker.closed?

          @worker = IO.popen(["node", WORKER_PATH], "r+")
          @worker.set_encoding(Encoding::UTF_8)
          at_exit { reset_worker } unless @at_exit_registered
          @at_exit_registered = true
          @worker
        end

        def self.reset_worker
          return unless @worker

          @worker.close unless @worker.closed?
        rescue IOError
          nil
        ensure
          @worker = nil
        end

        private_class_method :render, :ensure_worker, :reset_worker
      end
    end
  end
end
