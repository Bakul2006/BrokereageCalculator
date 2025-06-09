from flask import Flask, render_template, request

app = Flask(__name__)

def calculate_brokerage(data):
    buy_price = float(data['buy_price'])
    sell_price = float(data['sell_price'])
    quantity = int(data['quantity'])
    trade_type = data['trade_type']

    turnover = (buy_price + sell_price) * quantity


    if trade_type == 'delivery':
        brokerage = 0.0
    else:
        brokerage = min(20, 0.0003 * turnover)


    if trade_type == 'delivery':
        stt = 0.001 * sell_price * quantity
    else:
        stt = 0.00025 * sell_price * quantity

    txn_charge = 0.0000345 * turnover
    gst = 0.18 * (brokerage + txn_charge)

    sebi_charge = 0.000001 * turnover


    if trade_type == 'delivery':
        stamp_duty = 0.00015 * buy_price * quantity
    else:
        stamp_duty = 0.00003 * buy_price * quantity

    # Total Charges
    total_charges = brokerage + stt + txn_charge + gst + sebi_charge + stamp_duty

    # Net P&L
    profit_loss = (sell_price - buy_price) * quantity - total_charges

    return {
        'brokerage': round(brokerage, 2),
        'stt': round(stt, 2),
        'txn_charge': round(txn_charge, 2),
        'gst': round(gst, 2),
        'sebi_charge': round(sebi_charge, 2),
        'stamp_duty': round(stamp_duty, 2),
        'total_charges': round(total_charges, 2),
        'net_pl': round(profit_loss, 2)
    }

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    if request.method == 'POST':
        result = calculate_brokerage(request.form)
    return render_template('index.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)
