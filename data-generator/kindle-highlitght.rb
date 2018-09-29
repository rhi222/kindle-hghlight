require 'kindle_highlights'
require 'dotenv'
require 'json'
# for debug
# require 'pp'

Dotenv.load


kindle = KindleHighlights::Client.new(
  email_address: ENV["MAIL_ADDRESS"],
  password: ENV["PASSWORD"],
  root_url: "https://read.amazon.co.jp"
)

def generate_book_hash(kindle, output_hash, books)
  # 形式は下記
  # output_hash = {
  #   'asin' => {
  #     asin: xxxxx
  #     author: name
  #     title: great book title
  #     highlights: [
  #       {
  #         text: aaaaa,
  #         locaton: 111
  #       },....
  #     ]
  #   },....
  # }
  #
  books.each{ |book|
    book_info = {
      asin: book.asin,
      title: book.title,
      author: book.author,
      highlights: arrange_highlight_list(kindle, book.asin)
    }
    output_hash[book.asin] = book_info
  }
  return output_hash
end

def arrange_highlight_list(kindle, asin)
  highlights = kindle.highlights_for(asin)
  highlights.map{ |h|
    {
      text: h.text,
      location: h.location
    }
  }
end


## main
if __FILE__ == $0
  books = kindle.books
  output_hash = {}
  generate_book_hash(kindle, output_hash, books)
  # for debug
  # pp output_hash
  # puts JSON.pretty_generate(output_hash)
  path = __dir__ + "/kindle.json"
  File.open(path, "w") do |f|
    # f.write(output_hash.to_json)
    f.write(JSON.pretty_generate(output_hash))
  end
end
