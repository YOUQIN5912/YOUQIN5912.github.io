# UiO VASP Wiki 迁移记录

本次改动仅在独立分支中准备，不合并、不部署。网站新增界面、说明和按钮均为英文；本文件是供维护者阅读的中文报告，不生成网站页面。

## 恢复范围

- ZIP 中有 11 个有效文件和 11 个 `__MACOSX` 元数据文件。所有有效文件均按原始字节保存，并记录 SHA-256；原 ZIP 不修改。
- XML 恢复四页：Main Page、Getting started、Methods、Software and resources。每页仅有一个修订，共 66 个小节锚点、70 个代码块、5 张表格、8 条脚注参考文献。
- 四份 DOCX、四份 PDF 共 22 页用于交叉检查；66 个章节标题均可在相应 DOCX 和 PDF 导出中定位。此标题覆盖检查不等于每个字符均与 XML 相同。
- PDF 有明显的二次转换问题：shell 注释被排为大标题、`$SCRATCH` 被误作公式。代码以 XML 为准。DOCX 中的 comments.xml 为无实际评论的空结构，没有发现修订标记。
- Excel 有 Structure 和 Sheet1 两个工作表，含示例数据、k 点与超胞公式及任务日志表头，未发现真实作业明细；不改公式、不替换原文件。
- CatMAP 原图只有 940×450 像素，右侧列和底部行未完整截取；保留原图，不猜测被截掉的数据。

## 网站实现

- `/vasp-wiki/` 作为入口，另有 Getting Started、Computational Methods、Software & Resources、Sources & Recovery、Contributing & Future Tutorials，共六页。
- 顶部新增 VASP Wiki，采用现有网站配色与字体；Wiki 独立加载样式和脚本，提供分级侧栏、章节锚点、表格横向滚动、代码高亮及复制按钮、移动端布局。
- 所有原始页面显示历史说明、原始标题、修订时间、导出记录中的最后编辑者。原数据仅能支持“最后编辑者”，不能推断完整作者名单。
- Main Page 的嵌入内容改为章节链接；旧 Wiki 内部链接和 Main Page 的 NEB 片段链接改至新页面。OVITO URL 的尾随竖线与 `doi-org` 地址拼写在链接目标中修复，原文仍可下载核对。
- 未更改现有 Research、Publications、Software、News、CV 的正文。仅新增 Wiki 导航及仅在 Wiki 页启用的 CSS 引用。
- 未来 Olivia/NRIS、VASP 6、DFT、NEB、AIMD 以明确的 planned topics 预留；不伪装成已恢复或已验证教程。

## 仍无法恢复

1. 四个当前修订之前的历史、完整作者名单、讨论页以及未导出的其他页面。
2. `/cluster/projects/nn4604k/vasptest/` 的完整输入文件，独立 jobfile、完整 INCAR/KPOINTS/POSCAR/CONTCAR、VTST 工具和集群目录中的文件。
3. POTCAR 数据不在备份中；本次没有添加受 VASP 许可限制的数据。
4. CatMAP 原始 energies.txt、截图外的表格内容，以及任何未包含的图片和附件。
5. 原来就未完成的 convergence、benchmark、relaxation、error messages 和分子结合能表格内容。

## 授权与敏感信息

用户确认其为原课题组成员并可以使用这些资料。保留来源、编辑者身份和第三方权利，不将组内使用权限扩张为任何新公共许可证。备份中未找到明确的再发布许可证；需要进一步分发时仍应核对适用条款。

检查了源文本、DOCX 元数据/评论、PDF 元数据及 Excel 单元格。未发现密码、API token、私钥或真实作业日志；原文仍包含机构账号标识、姓名、课题组 allocation 编号，截图顶部也包含原账号及集群路径，均已在 Sources & Recovery 中说明。该检查不能证明绝无敏感信息。

## 技术内容的边界

保留所有原始参数、命令、路径和代码注释，包括明显需要复核的示例。特别标注 IDPP 的 `sort_tol=1.0)new_path` 连写问题；不擅自修改原例。Saga 指令没有被当作当前操作指南。外部链接及参考文献保留，但没有对所有旧网页、软件 API 或科学建议做逐条现时验证。

构建与链接检查结果见本 PR 的 VASP Wiki checks。构建流程只创建审核预览 artifact，不包含部署步骤。合并和正式上线仍需用户确认。

共享页头原已引用 14 个不存在的图标路径，其中 13 个为 link 目标、1 个为 metadata 内容。具体列表见 known-existing-issues.json。此次不修复这些既有问题；验证器对已列明路径单独报告，其他新增链接仍须全部通过检查。
