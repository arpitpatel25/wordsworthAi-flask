from flask import Flask, request, jsonify
from mongoengine import connect, DoesNotExist
from flask_cors import CORS  # Import CORS
from config import Config
from filter.openai_transcript import generate_transcript
from models.media_url import MediaUrl
from filter.apply_filters_5 import apply_filters
from filter.get_filter_values import get_brand_filters_service

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
connect(db='wordsworthai', host=Config.MONGO_URI)

@app.route('/filter_media', methods=['GET'])
def filter_media():
    query = MediaUrl.objects
    print(request.args)
    filtered_query = apply_filters(query, request.args)
    results = [
        {**media_url.to_mongo().to_dict(), '_id': str(media_url.id)}  # Convert ObjectId to string
        for media_url in filtered_query
    ]
    response = {
        "count": len(results),
        "results": results
    }
    return jsonify(response), 200

@app.route('/get_brand_filters', methods=['GET'])
def get_brand_filters():
    brand_url = request.args.get('brand_url')
    # brand_url = request.json.get('brand_url')

    print(brand_url)
    filters = get_brand_filters_service(brand_url)
    if filters is None:
        return jsonify({"message": "Brand URL not present"}), 404
    return jsonify(filters), 200

@app.route('/filter_media_page', methods=['GET'])
def filter_media_page():
    query = MediaUrl.objects
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 20))

    filtered_query = apply_filters(query, request.args)

    # Remove duplicates based on media_url
    unique_results = []
    seen_media_urls = set()

    for media_url in filtered_query:
        if media_url.media_url not in seen_media_urls:
            seen_media_urls.add(media_url.media_url)
            unique_results.append(media_url)

    total_results = len(unique_results)
    start = (page - 1) * per_page
    end = min(start + per_page, total_results)

    paginated_query = unique_results[start:end]

    results = [
        {**media_url.to_mongo().to_dict(), '_id': str(media_url.id)}
        for media_url in paginated_query
    ]

    response = {
        "count": total_results,
        "page": page,
        "per_page": per_page,
        "results": results
    }
    return jsonify(response), 200


@app.route('/generate_transcript', methods=['POST'])
def generate_video_transcript():
    try:
        # Extract parameters from the request
        openai_api_key = request.json.get('openai_api_key')
        video_url = request.json.get('video_url')
        mediaobject_id = request.json.get('mediaobject_id')

        # Validate parameters
        if not openai_api_key:
            return jsonify({"error": "OpenAI API key is missing."}), 400

        if not video_url:
            return jsonify({"error": "Video URL is missing."}), 400

        if not mediaobject_id:
            return jsonify({"error": "MediaObject ID is missing."}), 400

        # Check if the URL points to a video (basic validation based on file extension)
        if not video_url.endswith(('.mp4', '.avi', '.mov', '.mkv', '.webm')):
            return jsonify({"error": "The provided URL is not a video."}), 400

        # Retrieve the MediaUrl object
        try:
            media_url_obj = MediaUrl.objects.get(id=mediaobject_id)
        except DoesNotExist:
            return jsonify({"error": "MediaObject ID does not exist."}), 404

        # Check if the media type is video
        if media_url_obj.media_type != 'video':
            return jsonify({"error": "The media type is not a video."}), 400

        # Generate the transcript using the Whisper API
        is_success, result = generate_transcript(openai_api_key, video_url)

        if not is_success:
            return jsonify({"error": result}), 500

        # Update the MediaUrl object with the transcript
        media_url_obj.video_transcript = result
        media_url_obj.save()

        # Return the updated object
        response = media_url_obj.to_mongo().to_dict()
        response['_id'] = str(media_url_obj.id)
        return jsonify(response), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/generate_transcript_test', methods=['POST'])
def generate_video_transcript_test():
    try:
        openai_api_key = request.json.get('openai_api_key')
        video_url = request.json.get('video_url')

        if not openai_api_key:
            return jsonify({"error": "OpenAI API key is missing."}), 400

        if not video_url:
            return jsonify({"error": "Video URL is missing."}), 400

        if not video_url.endswith(('.mp4', '.avi', '.mov', '.mkv', '.webm')):
            return jsonify({"error": "The provided URL is not a video."}), 400

        is_success, result = generate_transcript(openai_api_key, video_url)

        if not is_success:
            return jsonify({"error": result}), 500


        return jsonify({"transcript": result}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)
