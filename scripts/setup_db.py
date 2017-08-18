import sqlite3

conn = sqlite3.connect('olx_re_data/sql/olx_re_data.db')
c = conn.cursor()

# Create table
c.execute('''CREATE TABLE listings
             (title text, creator text, creator_address text, 
             price real, for_rent boolean, post_address text,
             condition text, beds integer, baths integer,
             floor_size integer, ad_id real primary key)''')

conn.commit()
conn.close()