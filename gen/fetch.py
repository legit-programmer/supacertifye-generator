# import psycopg2
# from.import gen

# g = gen.Gen()
# def runner():
#     conn = psycopg2.connect(database="defaultdb", user="metalooze", password="pzI3YW988XNteAjtAlwugA", host="tantra-2k23-4240.8nk.cockroachlabs.cloud", port="26257")
#     print("db connected succesfully✅")

#     cur = conn.cursor()

#     # cur.execute("SELECT table_name FROM INFORMATION_SCHEMA.TABLES WHERE table_type = 'BASE TABLE'")
#     cur.execute("SELECT * FROM modelmakingdata")
#     teams = cur.fetchall()

#     for team in teams:
#         teamId = team[1]        
#         cur.execute(f"SELECT firstname, lastname, class FROM collegeuser WHERE teamid='{teamId}'")
#         members = cur.fetchall()
#         for member in members:
#             name = f"{member[0]} {member[1]}"
#             classs = member[2]
            
#             status = team[2]

#             g.generator(name, classs, status)
        
