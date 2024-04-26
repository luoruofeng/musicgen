# musicgen
使用meta开源模型生成指定格式，指定数量的音乐

# 打包
安装依赖前放开`requirements.txt`的注释
```
pip install -r requirements.txt
```
然后恢复注释后再执行
```
pip install .
```

# 使用方法
```
musicgen -d 'acoustic, guitar, melody, trap, d minor, 90 bpm' -f 'abc' -n 2
```
音频生成到了项目的music文件夹中