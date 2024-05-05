import sys
import cgi
import os
import math
import mimetypes
import json

from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse

import Physics




table_start = Physics.Table() 

first_shot = table_start.addBalls()

class MyHandler(BaseHTTPRequestHandler):


    def do_GET(self):

        parsed = urlparse(self.path)

        if parsed.path.startswith('/'):
            filepath = '.' + self.path  
            if os.path.isfile(filepath):
              
                mimetype, _ = mimetypes.guess_type(filepath)
                try:
                    with open(filepath, 'rb') as file:
                        content = file.read().decode('utf-8')
                    
                    svg_content = first_shot.svg()
                
                    content = content.replace('<!-- SVG_CONTENT -->', svg_content)
                    self.send_response(200)
                    self.send_header('Content-type', mimetype or 'application/octet-stream')
                    self.end_headers()
                    self.wfile.write(content.encode('utf-8'))
                except FileNotFoundError:
                    self.send_error(404, 'File Not Found: %s' % self.path)
        
        elif parsed.path.endswith(".html"):
            try:
                with open('.' + self.path, 'r') as file:
                    content = file.read()
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.send_header("Content-length", len(content))
                self.end_headers()
                self.wfile.write(bytes(content, "utf-8"))
            except FileNotFoundError:
                self.send_error(404, 'File Not Found: %s' % self.path)
                
        elif parsed.path.endswith(".js"):
            try:
                with open('.' + self.path, 'rb') as file:
                    content = file.read()
                self.send_response(200)
                self.send_header("Content-type", "application/javascript")
                self.send_header("Content-length", len(content))
                self.end_headers()
                self.wfile.write(content)
            except FileNotFoundError:
                self.send_error(404, 'File Not Found: %s' % self.path)

        elif parsed.path.startswith('/table-') and parsed.path.endswith('.svg'):
            # Serve SVG files
            table_file = parsed.path[1:]
            #print(table_file)
            if os.path.exists(table_file):
                with open(table_file, 'rb') as file:
                    content = file.read()
                    #print("CONTENT: ", str(content))
                self.send_response(200)
                self.send_header('Content-type', 'image/svg+xml')
                self.end_headers()
                self.wfile.write(content);
                
            else:
                self.send_error(404, 'File Not Found: %s' % self.path)


        else:
            # generate 404 for GET requests that aren't the 3 files above
            self.send_response( 404 );
            self.end_headers();
            self.wfile.write( bytes( "404: %s not found" % self.path, "utf-8" ) );


    def do_POST(self):

        parsed = urlparse(self.path) #get data by parsing url

        if parsed.path in ['/shot']:

            global first_shot
            global html_content

            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')


            #conver the sent data from json into python
            parsed_data = json.loads(post_data)
            velocity_x = parsed_data['velocity_x']
            velocity_y = parsed_data['velocity_y']

            print("velocity data: x =", velocity_x, ", y =", velocity_y)  # Add this line for debugging

            html_content = "<html><head><title>Pool Game</title><link rel='stylesheet' href='style.css'>"
            html_content += "<script src='https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js'></script><script src='shotLogic.js'></script></head><body>"

            
            game = Physics.Game(gameName=gameName, player1Name=player1Name, player2Name=player2Name)
            
            svg_tables, table = game.shoot(gameName, player1Name, initial_svg_content, velocity_x, velocity_y)

            first_shot = table
            html_content += f"""<div id="svgContainer" style="position: relative;">"""

            # Concatenate SVGs with a delimiter
            svg_data = ''.join(svg_tables)

            html_content += f"""<input type="hidden" id="svgData" value="{svg_data}">"""

            html_content += "</div>"
            html_content += '</body></html>' 

            #write_file(html_content)
            # Writing directly to animate.html
            with open('animate.html', 'w') as file:
                file.write(html_content)

                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(html_content.encode('utf-8'))

            
        # this is to get form that allows users to input names for players
        if parsed.path in ['/start-game']:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
          
            parsed_data = json.loads(post_data)
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"message": "Success"}).encode('utf-8'))


  


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 server.py <port#>")
        sys.exit(1)

    try:
        port = int(sys.argv[1])
    except ValueError:
        print("Invalid port number. Please provide a valid integer port.")
        sys.exit(1)

    db = Physics.Database(True)
    db.createDB()  # Initialize your database

    server_address = ('localhost', port)
    httpd = HTTPServer(server_address, MyHandler)  
    
   
    MyHandler.db = db 

    print(f"Server listening on port: {port}")
    httpd.serve_forever()