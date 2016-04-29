import time
import BaseHTTPServer
import json
import psycopg2

HOST_NAME = ''
PORT_NUMBER = 14242

# database
USERS = []
MESSAGES = []

class MyHandler(BaseHTTPServer.BaseHTTPRequestHandler):

    def do_HEAD(s):
        s.send_response(200)
        s.send_header("Content-type", "text/html")
        s.end_headers()
    def do_GET(s):
        '''Respond to a GET request.'''
        s.send_response(200)
        s.send_header("Content-type", "text/html")
        s.end_headers()
        print s.headers
        print s.path
        s.wfile.write("Ball.")
    def do_POST(s):
        '''Respond to a POST request.'''
        s.send_response(200)
        s.send_header("Content-type", "text/html")
        s.end_headers()
        # read complete body
        insize = s.headers.get('content-length',1)
        inp = s.rfile.read(int(insize))
        # examine body, create response
        response = process_input(inp)
        s.wfile.write(response)

def process_input(inp):
    '''decode json and react depending on command'''
    new_input = json.loads(inp)
    name = new_input['name']
    command = new_input['command']
    conn = psycopg2.connect("host='localhost' dbname='chat' user='postgres' password='12345'")
    cur = conn.cursor()
    cur.execute("SELECT name FROM users WHERE name = '" + name + "'")
    if cur.fetchone() == None:
	cur.execute("INSERT INTO users (name) VALUES ('" + name +"')")
	conn.commit()
    if command == 'update_contacts':
        if not name in USERS:
            USERS.append(name)
        response = json.dumps(
            {
                'command'  : 'update_contacts',
                'contacts' : USERS
            }
        )
    elif command == 'fetch_conversation':
        convers_partner = new_input['convers_partner']
        messages = []

        #for message in MESSAGES:
            #if (message[0] == name) and (message[1] == convers_partner):
            #    messages.append(message)
            #if (message[0] == convers_partner) and (message[1] == name):
            #    messages.append(message)
	
	uid = str(getID(cur,name))
	cpid = str(getID(cur,convers_partner))

	cur.execute("(SELECT msg as nachr, time as zeit, name FROM messages, users "
		    + "WHERE userid_1 = " + uid + " AND userid_2 = " + cpid
		    + " AND messages.userid_1 = users.user_id"
		    + " UNION ALL "
		    + "SELECT msg, time, name FROM messages, users " 
		    + "WHERE userid_1 = " + cpid + " AND userid_2 = " + uid
		    + " AND messages.userid_1 = users.user_id"
		    + ") order by zeit")
	message = cur.fetchall()
	for mess, zeit, name in message:
		messages.append((name,mess))
	
        response = json.dumps(
            {
                'command' : 'fetch_conversation',
                'messages' : messages
            }
        )
    elif command == 'send_msg':
        convers_partner = new_input['convers_partner']
        msg = new_input['msg']
        #MESSAGES.append((name, convers_partner, msg, time.asctime()))
	cur.execute("INSERT INTO messages (userid_1, userid_2, msg) "
		  + "VALUES ("+ str(getID(cur,name)) + ", " + str(getID(cur,convers_partner)) + ", '" + msg + "')")
	conn.commit()
	response = 'OK'
        response = json.dumps(
            {
                'command' : 'OK',
            }
        )
    else:
        response = 'OK'
    return response

def getID(cursor, user):
    cursor.execute("SELECT user_id FROM users WHERE name = '" +user+ "'")
    uid = cursor.fetchone()
    if uid != None:
	return uid[0]
    else:
	return None

if __name__ == '__main__':
    server_class = BaseHTTPServer.HTTPServer
    httpd = server_class((HOST_NAME, PORT_NUMBER), MyHandler)
    print time.asctime(), "Server Starts - %s:%s" % (HOST_NAME, PORT_NUMBER)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print time.asctime(), "Server Stops - %s:%s" % (HOST_NAME, PORT_NUMBER)
