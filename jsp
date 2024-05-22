了解了您的需求后，我们可以扩展之前的代码，不仅提取 Struts 标签，还提取其他 HTML 标签如 `table`、`div` 等。我们可以使用 `BeautifulSoup` 库来提取这些标签，并使用正则表达式来匹配特定前缀的自定义标签（例如 Struts 标签）。

以下是一个更全面的示例，展示如何读取 JSP 文件并提取和分析所有标签，包括标准 HTML 标签和 Struts 标签。

### 1. 读取 JSP 文件内容

```python
def read_jsp_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

jsp_content = read_jsp_file('path/to/your/file.jsp')
```

### 2. 提取所有标签

使用 `BeautifulSoup` 提取所有 HTML 标签和 Struts 标签：

```python
from bs4 import BeautifulSoup
import re

def extract_all_tags(jsp_content):
    soup = BeautifulSoup(jsp_content, 'html.parser')
    
    # 提取所有标签
    all_tags = soup.find_all(True)
    
    # 进一步分类
    struts_tags = []
    html_tags = []
    for tag in all_tags:
        if re.match(r'^s:', tag.name):
            struts_tags.append(tag)
        else:
            html_tags.append(tag)
    
    return struts_tags, html_tags

struts_tags, html_tags = extract_all_tags(jsp_content)

print("Struts Tags:")
for tag in struts_tags:
    print(tag)

print("\nHTML Tags:")
for tag in html_tags:
    print(tag)
```

### 3. 提取标签的属性

提取每个标签的属性以了解其配置：

```python
def extract_tag_attributes(tags):
    tag_attributes = []
    for tag in tags:
        tag_attributes.append({ 'tag': str(tag), 'attributes': tag.attrs })
    return tag_attributes

struts_tag_attributes = extract_tag_attributes(struts_tags)
html_tag_attributes = extract_tag_attributes(html_tags)

print("Struts Tag Attributes:")
for tag_info in struts_tag_attributes:
    print("Tag:", tag_info['tag'])
    print("Attributes:", tag_info['attributes'])

print("\nHTML Tag Attributes:")
for tag_info in html_tag_attributes:
    print("Tag:", tag_info['tag'])
    print("Attributes:", tag_info['attributes'])
```

### 4. 综合分析所有标签

将所有功能综合到一个分析函数中：

```python
def analyze_all_tags(file_path):
    jsp_content = read_jsp_file(file_path)
    
    struts_tags, html_tags = extract_all_tags(jsp_content)
    
    print("Struts Tags:")
    for tag in struts_tags:
        print(tag)
    
    print("\nHTML Tags:")
    for tag in html_tags:
        print(tag)
    
    struts_tag_attributes = extract_tag_attributes(struts_tags)
    html_tag_attributes = extract_tag_attributes(html_tags)
    
    print("\nStruts Tag Attributes:")
    for tag_info in struts_tag_attributes:
        print("Tag:", tag_info['tag'])
        print("Attributes:", tag_info['attributes'])
    
    print("\nHTML Tag Attributes:")
    for tag_info in html_tag_attributes:
        print("Tag:", tag_info['tag'])
        print("Attributes:", tag_info['attributes'])

# 调用分析函数
analyze_all_tags('path/to/your/file.jsp')
```

### 示例 JSP 文件

假设有一个示例的 JSP 文件 `example.jsp` 内容如下：

```jsp
<%@ taglib prefix="s" uri="/struts-tags" %>
<html>
<head>
    <title>Struts Example</title>
</head>
<body>
    <s:form action="login">
        <s:textfield name="username" label="Username" />
        <s:password name="password" label="Password" />
        <s:submit value="Login" />
    </s:form>
    <table>
        <tr><td>Row 1, Cell 1</td><td>Row 1, Cell 2</td></tr>
        <tr><td>Row 2, Cell 1</td><td>Row 2, Cell 2</td></tr>
    </table>
    <div id="content">
        <p>This is a paragraph inside a div.</p>
    </div>
</body>
</html>
```

使用上述代码来分析这个文件，输出将包括所有 HTML 标签和 Struts 标签及其属性。

### 总结

通过上述步骤，我们使用 Python 和 `BeautifulSoup` 解析 JSP 文件中的所有标签，包括 Struts 标签和标准 HTML 标签，并提取标签的属性信息。这可以帮助我们分析和理解 JSP 文件中的结构和动态内容。根据需要，可以进一步扩展这些功能，例如处理更多自定义标签或添加更复杂的分析逻辑。