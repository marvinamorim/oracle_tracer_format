import sqlparse

lines = open('faturamento_demora.log','r')
parsed = open('statments.sql', 'w+')
text = ''
for line in lines:
    text += line

statements = text.split('Time: ')
oexec = []
count = 0
statement_count = 0
for statement in statements:
    if ' oexec ' in statement:
        statement = statement.split('\n')
        
        statement.pop(0)
        statement = '\n'.join(statement)
        binds = len(statement.split(' :'))-1
        bind_count = 1
        for full_bind in statements[count+1:count+binds+1]:
            bind = full_bind.split('\n')
            bind.pop(0)
            statement = statement.replace(f':{bind_count}',bind[0]+f'  /*bind {bind_count}*/')
            bind_count += 1
        statement += ';\n--------------------------------------------------------------------\n'
        parsed.write(sqlparse.format(statement, reindent=True, keyword_case='upper'))
        statement_count += 1

    count += 1
print(f'\n\n--Total statements: {statement_count}')
parsed.write(f'\n\n--Total statements: {statement_count}')
lines.close()
parsed.close()