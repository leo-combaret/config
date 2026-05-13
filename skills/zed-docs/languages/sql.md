# SQL
SQL files are handled by the SQL Extension .
- Tree-sitter: nervenes/tree-sitter-sql
### Formatting
Zed supports auto-formatting SQL using external tools like sql-formatter .
1. Install sql-formatter :
```
npm install -g sql-formatter
```
1. Ensure sql-formatter is available in your path and check the version:
```
which sql-formatter
sql-formatter --version
```
1. Configure formatting in Settings ( cmd-,|ctrl-, ) under Languages > SQL, or add to your settings file:
```
"languages": {
    "SQL": {
      "formatter": {
        "external": {
          "command": "sql-formatter",
          "arguments": ["--language", "mysql"]
        }
      }
    }
  },
```
Substitute your preferred [SQL Dialect] for mysql above ( duckdb , hive , mariadb , postgresql , redshift , snowflake , sqlite , spark , etc).
You can add this to Zed project settings ( .zed/settings.json ) or via your Zed user settings ( ~/.config/zed/settings.json ).
### Advanced Formatting
Sql-formatter also allows more precise control by providing sql-formatter configuration options . To provide these, create a .sql-formatter.json file in your project:
```
{
  "language": "postgresql",
  "tabWidth": 2,
  "keywordCase": "upper",
  "linesBetweenQueries": 2
}
```
When using a .sql-formatter.json file you can use a simplified Zed settings configuration:
```
{
  "languages": {
    "SQL": {
      "formatter": {
        "external": {
          "command": "sql-formatter"
        }
      }
    }
  }
}
```