---
sidebar_position: 7
title: "图像处理"
---

# 📸 批量处理图像

对一个文件夹的图像进行调整大小、添加水印、格式转换或生成缩略图。

> **你：** $Image Processor <br/>
> /photos 中有产品图片。将它们调整到 800x800，添加水印，并制作缩略图。

## AI 的工作流程

1. 使用 PIL/Pillow（预装）处理所有图像
2. 创建带水印的原始大小版本
3. 按要求大小创建缩略图
4. 生成联系表（所有缩略图的网格）
5. 报告文件数量和大小节省情况

{/* TODO: Screenshot — File browser showing three output folders: processed/ (watermarked), thumbnails/ (200x200), plus a contact_sheet.png previewed as a grid of product images. */}

## 技能内容

将下面的内容复制到**工作区 → 技能 → 创建**：

```markdown
---
name: image-processor
description: Batch processes images - resize, watermark, convert, and generate thumbnails
---

## Image Processing

When processing images:

1. **Survey first**: Count files, check formats, note total size
2. **Process one file as a test**: Show the result before processing the rest
3. **Use Pillow (PIL)**:
   - Resize with aspect ratio preservation (use thumbnail or fit)
   - Watermarks: semi-transparent text in lower-right corner
   - Format conversion: handle RGBA→RGB for PNG→JPEG
4. **Organize output** into clear subdirectories (processed/, thumbnails/, etc.)
5. **Generate a summary**: files processed, size before/after
6. **For large batches**, report progress: "Processed 25/50..."

Always preview the first result before batch-processing.
```
