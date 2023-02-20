import xml.etree.cElementTree as ET
from urllib import request

########################################################
#
#  1) put your nexus xml credentials here (replace the strings of zeros with your id and code from
# https://phoenixbse.com/index.php?a=user&sa=xml
#  (full, not the offline editor)
#

xml_id = '000'
xml_code = '000o0000o0000o0000o0000o0000o000'


######################################################
#
#   2)  change this bit to point to your email.trn file
#    (use full file path if not in same folder as this script)

trn_file = 'TURN121922_test.TRN'

######################################################

#
#   3) run the file, hopefully should give a message with some turn ids
#    but go into nexus -> orders -> sent turns and eyeball one or two of them to double check.

#######################################################


def start_orders():
    turns = ET.Element('turns')
    return turns


def make_turns(orders_xml, position_number, order_list, append, seq):
    if seq[0] == '0':
        sequence = '0'
        seq_after = '0'
    else:
        sequence = '1'
        seq_after = str(seq[0])
    turns = orders_xml
    turn = ET.SubElement(turns, 'turn', pos_id=position_number, append="false")  # a single position
    orders = ET.SubElement(turn, 'orders') # orders collection for a position
    for item in order_list:
        order = ET.SubElement(orders
                              , 'order'
                              , id=str(item[0])
                              , issue_type=str(item[1])
                              , seq=sequence
                              , seq_after=seq_after
                              )
        for p in item[2:]:
            param = ET.SubElement(order, 'param').text = str(p)
    return orders_xml


def send_turns(xml_id, xml_code, xml_orders_string):
    base_url = 'https://www.phoenixbse.com/index.php?a=xml&uid={}&code={}&sa={}'
    send_url = base_url.format(xml_id, xml_code, 'send_orders')
    data = xml_orders_string.encode('utf-8')
    req = request.Request(send_url, data=data)
    r = request.urlopen(req).read().decode('utf-8')
    return r


def reformat_trn_order(trn_order_str):
    # receive a single order line from the trn file
    # for example:   'Order=2240,0,0,16,26; // GPI Sector'
    # want to get the numbers between the = and the ;
    # then convert into a list

    trn_order_str = trn_order_str[6:].split(';')[0].split(',')
 
    return trn_order_str


def parse_trn_file(file_path, orders_xml):
    start_of_file = True
    with open(file_path, 'r') as f:
        for row in f:
            if row[:6] == 'Order=':
                clean_order = reformat_trn_order(row)
                order_list.append(clean_order)
                next
            if row[:9] == 'Position=' and not start_of_file:
                # all orders for the previous position now collected, convert them to xml
                orders_xml = make_turns(orders_xml, position_number, order_list, "false", seq_array)
                # clean down the list and grab the new position number
                order_list = []
                position_number = row[9:].split(';')[0]
                next
            if row[:9] == 'Position=' and start_of_file:
                position_number = row[9:].split(';')[0]
                start_of_file = False
                order_list = []
                next
            if row[:9] == 'Sequence=':
                seq_array = row[9:].split(';')[0].split(',')




        # iteration finished, but should still be one last ship to sort out
        orders_xml = make_turns(orders_xml, position_number, order_list, "false", seq_array)

    return orders_xml


if __name__ == "__main__":
    orders_xml = start_orders()
    orders_xml = parse_trn_file(trn_file, orders_xml)
    orders_txt = ET.tostring(orders_xml, encoding='unicode', method='xml')
    y = send_turns(xml_id, xml_code, orders_txt)
    print(y)
