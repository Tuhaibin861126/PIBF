# GitHub 与 Streamlit 部署说明

## 一、上传 GitHub

1. 在 GitHub 新建一个空仓库，例如 `pibf-risk-calculator`。
2. 解压最终 ZIP 文件。
3. 将 `06_PUBLIC_STREAMLIT_CALCULATOR` 文件夹里面的全部文件上传到 GitHub 仓库根目录。
4. 不要只上传 `app.py`；`.streamlit`、`model_coefficients.json` 和 `risk_model.py` 也必须上传。

上传完成后，GitHub 仓库首页应直接看到：

- `app.py`
- `risk_model.py`
- `model_coefficients.json`
- `requirements.txt`
- `README.md`
- `.streamlit` 文件夹
- `tests` 文件夹

## 二、部署到 Streamlit Community Cloud

1. 登录 Streamlit Community Cloud。
2. 点击创建新应用。
3. 选择刚才上传的 GitHub 仓库。
4. Branch 选择 `main`。
5. Main file path 填写 `app.py`。
6. 点击 Deploy。

本项目不需要填写 Secrets，也不需要连接数据库。

## 三、部署后检查

1. 使用 `sample_cases.csv` 中的三个样例逐一测试。
2. 检查预测概率、风险分层和模型贡献图是否正常显示。
3. 分别用电脑和手机打开网页，检查排版。
4. 测试“Download result JSON”按钮。
5. 确认网页首屏保留“Research use only”声明。

## 四、文章中替换链接

部署成功后会得到类似下面的地址：

`https://YOUR-APP-NAME.streamlit.app`

用这个地址同时替换正文和回复信中的红色占位符：

`[WEB CALCULATOR URL TO BE PROVIDED BY AUTHORS]`

## 五、正式提交前

当前参数来自内部规划分析。正式公开或投稿前，必须使用最终真实数据库重新拟合并核对 `model_coefficients.json`、三个测试样例的期望概率、论文中的模型系数和全部验证结果。
