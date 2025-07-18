# 合并 PDF

这是一个用于将文档合并为单一输出 PDF 的 Python 脚本。非常适合快速打包扫描文档，无需安装带有此功能的扫描软件或手动通过 Microsoft Office 合并。

支持的格式：`pdf`、`png`、`jpeg`、`jpg`。

# 功能
- 合并多个文件为一个 `pdf`
- 从源 `pdf` 文件中提取指定页面

## 前置条件

- 安装 Python 3.6 及以上版本
- 在终端运行此文件

```bat
install.bat
```

## 命令

| 命令 | 描述 |
|------|------|
| `-merge` | 合并多个文件为一个 pdf。可选支持对 `pdf` 文件进行页面选择和页面范围选择。|
| `-blob`  | 通过指定源目录，将所有支持的文件合并为一个 pdf。合并内容按字母顺序排列。|

> 以上所有命令均需使用绝对文件路径或绝对目录路径。

## 示例
`-merge`

格式：
###
```cmd
python merge-pdf.py -merge <文件1> <文件2> -o <输出文件>
```
用例：
```cmd
python merge-pdf.py -merge "example.png [1, 3:5]" -o "../output.pdf"
```
目标文件将包含第1页、第3至第5页。

---

`-blob`

用例：
```cmd
python merge-pdf.py -blob <目录> -o <输出文件>
```



