
# DoDo2 

DoDo2 は静的なブログを作成するソフトウェアです。
このソフトウェアは、用意された記事データから、ブログに必要なファイル群を作成します。
また、適切な設定を行うことで、作成時にサイトマップの生成や、ファイルの圧縮、アップロードなども行ってくれます。

一見すると便利そうですが、このソフトウェアは実験的に書かれたものであり、未だ未完成です。
そのため、不具合だったり、プログラムに幾つかの課題を抱えています。
普通にブログが欲しい方は WordPress を導入するなり、既存のウェブサービスを使用したほうが良いでしょう。

## 使い方 

### ディレクトリの初期化

まずはブログを保存するためのディレクトリを作成し、初期化しましょう。
適当なディレクトリに移動して、下記のコマンドを実行してください。

```shell
mkdir example
cd example
dodo init 
```

初期化に成功すると、これらのファイル（ディレクトリ）が作成されます。

| file (directory) name | description | 
| --------------------- | ----------- | 
| cache                 | 一部のプログラムが使用するディレクトリです。このディレクトリは通常用途で使用されることはありません。 | 
| dist                  | 作成されたファイル群が保存されるディレクトリです。 | 
| src                   | 作成された記事のデータが保存されたディレクトリです。このディレクトリ内の記事を元に、ページが生成されます。 | 
| static                | 静的なファイルが保存されたディレクトリです。このディレクトリ内に置かれたファイルは、そのまま dist にコピーされます。 | 
| dodo.json             | ブログの広範な設定が書かれたファイルです。 | 

### 記事の作成

初期化が終わったら、記事を作成しましょう。
記事を作成するには `dodo create` コマンドを実行します。

```shell
dodo create hello-dodo
```

### 記事の編集

記事の作成に成功すると、これらのファイル（ディレクトリ）が作成されます。

* src/hello-dodo
* src/hello-dodo/config.json
* src/hello-dodo/full_text.json
* src/hello-dodo/summary_text.json

作成された記事は白紙です。
さっそく記事の内容を編集してみましょう。

```html
<!-- full_text.json -->
<h1>Hello DoDo!</h1>
<p>
  これは記事の全文です。
</p>
```

```html
<!-- summary_text.json -->
<h1>Hello DoDo!</h1>
<p>
  これは記事の概要です。
</p>
```

config.json も編集しましょう。
config.json は記事に関するデータを保存しています。
config.json の `title` パラメータを下記のように書き換えます。

```json
/* config.json */
{
  "title": "Hello DoDo!"
}
```

### テンプレートの作成

記事の編集は終わりましたか？
最後にブログの雛形となるテンプレートを作成しましょう。
下記のファイルを作成し static/template.html として保存しましょう。

```html
<!-- static/template.html -->
<!DOCTYPE html>
<html>
  <head>
    {% if page_type == "single" %}
      <title>{{ post.title }}</title>
    {% endif %}
  </head>
  <body>
    {% for post in posts %}
      {% if page_type == "single" %}
        {{ post.full_text }}
      {% else %}
        {{ post.summary_text }}
      {% endif %}
    {% endfor %}
  </body>
</html>
```

テンプレートの作成が終わったら dodo.json を編集しましょう。
dodo.json に `template` のパラメータを追加します。

```json
/* dodo.json */
{
  "template": {
    "class": "jinja2",
    "src": "static/template.html"
  }
}
```

### ページのビルド 

すべての作業が終わったら `dodo update` コマンドを実行します。
`dodo update` コマンドは用意された記事データから、必要なファイルを作成あるいは更新します。

```
dodo update
```

作成されたファイルは `dist` ディレクトリ以下に保存されます。
保存されたファイルをサーバに FTP 等でアップロードすることで、ブログを公開することができます。

また、下記のように、設定をすることで、更新時に差分をサーバにアップロードしてくれるようになります。
詳細は [dodo_ftp](dodo_ftp) のソースコードを読んでください。

```json
/* dodo.json */
{
  "ftp": {
    "servers": [
      {
        "host": "localhost",
        "port": 2121
      }
    ]
  }
}
```

更新作業お疲れさまでした。
だいたいの流れは以上になります。

一応パッケージ内に、[簡単なデモ](demo)が用意されているので、
具体的な使い方が知りたい方はそちらも読んでみると良いかもしれません。

## インストール方法 

setup.py を同梱しているので、下記のコマンドから導入することができます。

```
python setup.py install 
```

## ライセンス 

&copy; 2020 tikubonn

DoDo2 は GPLv3 ライセンスで公開されています。
