from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

# Хранилище объявлений
ads = {}

# Счетчик для ID объявлений
ads_counter = 1

@app.route('/ad', methods=['POST', 'GET', 'DELETE'])
def ad():
    global ads_counter
    if request.method == 'POST':
        # Создание объявления
        ad_data = request.json
        ad_id = ads_counter
        ads_counter += 1
        ads[ad_id] = {
            'title': ad_data.get('title'),
            'description': ad_data.get('description'),
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'owner': ad_data.get('owner')
        }
        return jsonify({'id': ad_id}), 201

    elif request.method == 'GET':
        # Получение списка объявлений
        ad_id = request.args.get('id')
        if ad_id:
            ad_id = int(ad_id)
            ad = ads.get(ad_id)
            if ad:
                return jsonify(ad), 200
            else:
                return jsonify({'error': 'Ad not found'}), 404
        else:
            return jsonify(list(ads.values())), 200

    elif request.method == 'DELETE':
        # Удаление объявления
        ad_id = request.args.get('id')
        if ad_id:
            ad_id = int(ad_id)
            if ad_id in ads:
                del ads[ad_id]
                return jsonify({'success': 'Ad deleted'}), 200
            else:
                return jsonify({'error': 'Ad not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
