#!/usr/bin/env python
from __future__ import print_function
from base_model import branchpoint_predict
import json
import pyjsonrpc
from bam2x.Annotation import BED12,BED6
import sqlite3
from bam2x.Struct import binindex
from bam2x.DBI.Templates import select_template as template
from bam2x.DBI.Templates import factories
from bam2x import TableIO,Tools
conn = sqlite3.connect("data/hg19_one_tr_per_gene.bed.db")
conn.row_factory=factories["bed12"]
cursor=conn.cursor()
s = "select * from gene"
cursor.execute(s)
r=cursor.fetchall()
h={}
DataS3=binindex(TableIO.parse("data/DataS3.uniq.bed.gz","bed6"))
genelist=[i.id for i in r] 
print(genelist)
for i in r:
    h[i.id]=i
	
class RequestHandler(pyjsonrpc.HttpRequestHandler):
  @pyjsonrpc.rpcmethod
  def add(self, a,b):
      """Test method"""
      return a + b
  @pyjsonrpc.rpcmethod
  def branch(self,seq):
      x=branchpoint_predict(seq)
      return x
  @pyjsonrpc.rpcmethod
  def introns(self,name): 
      if not h.has_key(name):
	  return []
      retv=[]
      r=h[name]
      for i in r.Introns():
	  if i.stop-i.start>60:
	     j=i.tail(60)
             v = [ Tools.translate_coordinate(j,d) for d in DataS3.query(j)]
	     retv.append({"chr":j.chr,"id":j.id,"start":j.start,"end":j.end,"strand":j.strand,"v":v})
      return retv
  @pyjsonrpc.rpcmethod 
  def list(self):
      return genelist
      
      
       
http_server = pyjsonrpc.ThreadingHttpServer(
    server_address = ('localhost', 7000),
    RequestHandlerClass = RequestHandler
)
print("Starting HTTP server ...")
print("URL: http://localhost:7000")
http_server.serve_forever()
