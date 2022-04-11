# This file contains the specifications for the API used in Project Alph.
# Desired functionality:
# 1) GET information about a document (source file, title, connections)
# 2) POST a new document to the pool to be parsed and added to the docgraph
# 3) PUT new information into a document, such as if the document is being read or not
# 4) GET the graph, updating everything
# API details:
# 1) Endpoints: /api/pool/

from flask import Flask
from flask_restful import Resource, Api, reqparse
from docgraph import DocGraph

APP = Flask(__name__)
API = Api(APP)

GRAPH = DocGraph()


class Pool(Resource):
    def get(self):
        """
        If nothing specified, just returns a representation of the graph.
        If file specified, then return information about that file.
        If update is True, make updates to the graph first.
        """
        # Get arguments from request
        parser = reqparse.RequestParser()
        parser.add_argument('title', type=str, required=False, default="")
        parser.add_argument('update', type=bool, default=False)
        args = parser.parse_args()

        if args['update']:
            print("Updating")
            GRAPH.make_all_graph_connections()

        if args['title']:
            # Return information about requested file
            print("Getting file")
            file_data = GRAPH.get_node(args['title']).get_info()
            edges = GRAPH.list_edges(args['title'])
            data = {"file_info": file_data, "connections": edges}
            return data, 200
        else:
            print("Getting graph")

        return {"data": "hello there", "tmp": "general kenobi", "list": [1, 2]}, 200

    def post(self):
        # Get arguments from request
        parser = reqparse.RequestParser()
        parser.add_argument('filepath', type=str,
                            required=True, help="filepath is required")
        parser.add_argument('main', type=bool, default=False)
        args = parser.parse_args()
        print(args)

        # Create new node
        GRAPH.add_node(args["filepath"], args["main"])
        print(GRAPH.list_nodes())

        return 200


API.add_resource(Pool, "/api/pool")
if __name__ == '__main__':
    APP.run(debug=True)
