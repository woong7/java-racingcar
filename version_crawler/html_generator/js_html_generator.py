from version_crawler.html_generator.html_generator import HTMLGenerator, create_table_from_rows


class JSHTMLGenerator(HTMLGenerator):

    def generate_html(self, rows, current_time):
        table_rows = create_table_from_rows(rows)

        html = f"""
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                body {{
                    font-family: Arial, sans-serif;
                }}
                .container {{
                    display: flex;
                    align-items: flex-start;
                    justify-content: center;
                    margin: 20px;
                }}
                .title {{
                    display: flex;
                    align-items: center;
                    font-size: 32px;
                    font-weight: bold;
                    margin-bottom: 20px;
                }}
                .title img {{
                    margin-right: 10px;
                    width: 180px;
                    height: 180px;
                }}
                .title-text {{
                    margin-left: 10px;
                }}
                .time {{
                    font-size: 16px;
                    margin-top: 5px;
                    color: #888;  
                    text-align: center;
                }}
                table {{
                    border-collapse: collapse;
                    flex: 1;
                    margin-right: 20px;
                    background-color: #f9f9f9;
                    border: 1px solid #ddd;
                    border-radius: 4px;
                }}
                th, td {{
                    padding: 10px;
                    border: 1px solid #ddd;
                    text-align: center;
                }}
                th {{
                    background-color: #f5f5f5;
                    cursor: pointer;
                }}
                .image-container {{
                    flex: 0 0 300px;
                }}
                .image-container p {{
                    font-weight: bold;
                    margin-bottom: 10px;
                    text-align: center;
                }}
                .image-divider {{
                    border-top: 1px solid #ddd;
                    margin-top: 20px;
                    padding-top: 10px;
                }}
            </style>
            <script>
                function sortTable(column) {{
                    const table = document.getElementById("repositories-table");
                    const rows = Array.from(table.rows).slice(1);  // 테이블 행을 배열로 변환하고 첫 번째 행(헤더) 제외
    
                    rows.sort(function(a, b) {{
                        const textA = a.cells[column].textContent.trim();
                        const textB = b.cells[column].textContent.trim();
                        return textA.localeCompare(textB, 'en', {{ numeric: true, sensitivity: 'base' }});
                    }});
    
                    // 정렬된 행을 테이블에 다시 추가
                    rows.forEach(function(row) {{
                        table.appendChild(row);
                    }});
                }}
            </script>
        </head>
        <body>
            <div class="container">
                <div class="title">
                    <img src="{self.s3_bucket_uri}/bep_logo.png" alt="Logo">
                    <div class="title-text">
                        Birdview JS Repositories Version Dashboard
                        <div class="time">Recently updated at {current_time}</div>
                    </div>
                    <img src="{self.s3_bucket_uri}/bep_logo.png" alt="Logo" style="transform: scaleX(-1);">
                </div>
            </div>
            <div class="container">
                <div>
                    <h2>Current Repositories Status</h2>
                    <p> -> Click on column title to sort by that column</p>
                    <table id="repositories-table">
                        <tr>
                            <th onclick="sortTable(0)">Repository</th>
                            <th onclick="sortTable(1)">Node Version</th>
                            <th onclick="sortTable(2)">TS Version</th>
                            <th onclick="sortTable(3)">Jest Version</th> 
                            <th onclick="sortTable(4)">Updated At</th>
                        </tr>
                        {table_rows}
                    </table>
                </div>
                
                <div class="image-container">
                    <p><a href="https://www.python.org/downloads/">Python Version Support</a></p>
                    <img src="{self.s3_bucket_uri}/python_version_info.png" alt="Python Version">
                    <div class="image-divider"></div>
                    <p><a href="https://www.djangoproject.com/download/">Django Version Support</a></p>
                    <img src="{self.s3_bucket_uri}/django_version_info.png" alt="Django Version">
                </div>
            </div>
        </body>
        </html>
        """
        return html
