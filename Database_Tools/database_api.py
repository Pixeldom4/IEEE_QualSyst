from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
CORS(app)

"""
Configure using SQLite database for testing. Will move to cloud when ready.
"""
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///research_papers.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

"""
These are the updated columns in the database.
"""
class ResearchPaper(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    article_title = db.Column(db.String, nullable=False)
    article_authors = db.Column(db.String, nullable=False)
    article_abstract = db.Column(db.Text, nullable=True)
    article_link = db.Column(db.String, nullable=True)
    search_terms = db.Column(db.String, nullable=True)


"""Creating the tables in the database."""
with app.app_context():
    db.create_all()

# API Endpoints
@app.route('/papers', methods=['POST'])
def add_paper():
    """ Add a new research paper."""
    data = request.json
    # Validate required fields
    if not data.get('article_title') or not data.get('article_authors'):
        return jsonify({"error": "article_title and article_authors are required fields"}), 400

    try:
        new_paper = ResearchPaper(
            article_title=data['article_title'],
            article_authors=data['article_authors'],
            article_abstract=data.get('article_abstract'),
            article_link=data.get('article_link'),
            search_terms=data.get('search_terms'),
        )
        db.session.add(new_paper)
        db.session.commit()
        return jsonify({"message": "Paper added successfully"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@app.route('/papers', methods=['GET'])
def get_papers():
    """ Retrieve all research papers."""
    try:
        papers = ResearchPaper.query.all()
        result = [
            {
                "id": paper.id,
                "article_title": paper.article_title,
                "article_authors": paper.article_authors,
                "article_abstract": paper.article_abstract,
                "article_link": paper.article_link,
                "search_terms": paper.search_terms,
            }
            for paper in papers
        ]
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/papers/search', methods=['GET'])
def get_paper_by_title():
    """ Search papers by title."""
    title = request.args.get('title')
    if not title:
        return jsonify([]), 200
    papers = ResearchPaper.query.filter(ResearchPaper.article_title.ilike(f"%{title}%")).all()
    result = [
        {
            "id": paper.id,
            "article_title": paper.article_title,
            "article_authors": paper.article_authors,
            "article_abstract": paper.article_abstract,
            "article_link": paper.article_link,
            "search_terms": paper.search_terms,
        }
        for paper in papers
    ]
    return jsonify(result), 200


if __name__ == '__main__':
    # Set the host and port
    host = '127.0.0.1'  # Localhost
    port = 5000         # Default Flask port

    # Print the API URL
    print(f"API is running at: http://{host}:{port}")

    # Run the Flask app
    app.run(debug=True, host=host, port=port)
