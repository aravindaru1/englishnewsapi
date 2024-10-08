import newspaper
from flask import Flask, request, jsonify
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

@app.route('/summarize', methods=['POST'])
def summarize_article():
    url = request.json.get('url')
    if not url:
        return jsonify({'error': 'URL is required'}), 400

    try:
        article = newspaper.Article(url)
        article.download()
        article.parse()
        article.nlp()

        img_url = article.top_image
        title = article.title
        full_text = article.text.replace('Advertisement', '')
        summary = article.summary.replace('Advertisement', '')

        return jsonify({
            'img_url': img_url,
            'title': title,
            'full_text': full_text,
            'summary': summary
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
