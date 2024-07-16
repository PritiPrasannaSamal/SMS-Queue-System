from flask import Flask, request, jsonify
import random



app = Flask(__name__)

@app.route('/sms-gateway', methods=['POST'])
def sms_gateway():
    data = request.get_json()
    
    name = data.get('name')
    contact_no = data.get('contact_no')
    message = data.get('message')
    
    x = random.randint(0,9)
    if x>7:
        status = "failure"
    else:
        status = "success"

    return jsonify({"status": status})



if __name__ == '__main__':
    app.run(debug=True)
    

