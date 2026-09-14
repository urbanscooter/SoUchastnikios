import os

# Корень проекта — текущая папка
ROOT = os.getcwd()

def write(path, content):
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"✓ {path}")

# === 1. project.yml ===
write("project.yml", """name: SoUchastnik
options:
  bundleIdPrefix: com.urbanscooter
  deploymentTarget:
    iOS: "16.0"
  createIntermediateGroups: true

targets:
  SoUchastnik:
    type: application
    platform: iOS
    sources:
      - App
      - Shared
    info:
      path: App/Info.plist
      properties:
        CFBundleDisplayName: СоУчастник
        UILaunchScreen: {}
        UIApplicationSceneManifest:
          UIApplicationSupportsMultipleScenes: false
    settings:
      base:
        PRODUCT_BUNDLE_IDENTIFIER: com.urbanscooter.souchastnik
        MARKETING_VERSION: "1.0"
        CURRENT_PROJECT_VERSION: "1"
        CODE_SIGN_IDENTITY: ""
        CODE_SIGNING_REQUIRED: "NO"
        CODE_SIGNING_ALLOWED: "NO"
    dependencies:
      - target: SoUchastnikKeyboard
        embed: true

  SoUchastnikKeyboard:
    type: app-extension
    platform: iOS
    sources:
      - Keyboard
      - Shared
    info:
      path: Keyboard/Info.plist
      properties:
        CFBundleDisplayName: СоУчастник
        NSExtension:
          NSExtensionPointIdentifier: com.apple.keyboard-service
          NSExtensionPrincipalClass: $(PRODUCT_MODULE_NAME).KeyboardViewController
          NSExtensionAttributes:
            IsASCIICapable: true
            PrefersRightToLeft: false
            PrimaryLanguage: ru
            RequestsOpenAccess: false
    settings:
      base:
        PRODUCT_BUNDLE_IDENTIFIER: com.urbanscooter.souchastnik.keyboard
        MARKETING_VERSION: "1.0"
        CURRENT_PROJECT_VERSION: "1"
        CODE_SIGN_IDENTITY: ""
        CODE_SIGNING_REQUIRED: "NO"
        CODE_SIGNING_ALLOWED: "NO"
""")

# === 2. Shared/ArticleDatabase.swift ===
write("Shared/ArticleDatabase.swift", '''import Foundation

public struct Article: Identifiable {
    public let id = UUID()
    public let code: String
    public let title: String
    public let fullText: String
    public let category: Category

    public enum Category: String {
        case koap = "КоАП РФ"
        case uk = "УК РФ"
    }
}

public enum ArticleDatabase {
    public static let dangerousWords: [String: Article] = [
        "дискредитация": Article(code: "Ст. 20.3.3 КоАП РФ", title: "Дискредитация ВС РФ", fullText: "Публичные действия, направленные на дискредитацию использования Вооруженных Сил Российской Федерации. Штраф для граждан от 30 000 до 50 000 рублей.", category: .koap),
        "фейк": Article(code: "Ст. 13.15 КоАП РФ", title: "Распространение фейков", fullText: "Распространение заведомо недостоверной общественно значимой информации под видом достоверных сообщений. Штраф от 30 000 до 100 000 рублей.", category: .koap),
        "хулиганство": Article(code: "Ст. 20.1 КоАП РФ", title: "Мелкое хулиганство", fullText: "Нарушение общественного порядка, выражающее явное неуважение к обществу. Штраф от 500 до 1 000 рублей или арест до 15 суток.", category: .koap),
        "митинг": Article(code: "Ст. 20.2 КоАП РФ", title: "Нарушение правил митинга", fullText: "Нарушение порядка организации митинга. Штраф от 10 000 до 20 000 рублей или обязательные работы до 40 часов.", category: .koap),
        "пикет": Article(code: "Ст. 20.2 КоАП РФ", title: "Нарушение правил пикетирования", fullText: "Нарушение порядка проведения публичного мероприятия. Штраф от 10 000 до 20 000 рублей.", category: .koap),
        "оскорбление": Article(code: "Ст. 5.61 КоАП РФ", title: "Оскорбление", fullText: "Унижение чести и достоинства другого лица в неприличной форме. Штраф от 1 000 до 3 000 рублей.", category: .koap),
        "наркотик": Article(code: "Ст. 6.8 КоАП РФ", title: "Незаконный оборот наркотиков", fullText: "Незаконное приобретение или хранение наркотических средств без цели сбыта. Штраф от 4 000 до 5 000 рублей или арест до 15 суток.", category: .koap),
        "пьяный": Article(code: "Ст. 12.8 КоАП РФ", title: "Вождение в нетрезвом виде", fullText: "Управление ТС в состоянии опьянения. Штраф 30 000 рублей и лишение прав от 1.5 до 2 лет.", category: .koap),
        "скорость": Article(code: "Ст. 12.9 КоАП РФ", title: "Превышение скорости", fullText: "Превышение скорости на 20–40 км/ч. Штраф 500 рублей.", category: .koap),
        "экстремизм": Article(code: "Ст. 282 УК РФ", title: "Возбуждение ненависти", fullText: "Возбуждение ненависти либо вражды, унижение достоинства человека или группы лиц. Штраф от 300 000 до 500 000 рублей или лишение свободы до 5 лет.", category: .uk),
        "взятка": Article(code: "Ст. 291 УК РФ", title: "Дача взятки", fullText: "Дача взятки должностному лицу. Штраф до 200 000 рублей или лишение свободы до 8 лет.", category: .uk),
        "клевета": Article(code: "Ст. 128.1 УК РФ", title: "Клевета", fullText: "Распространение заведомо ложных сведений, порочащих честь и достоинство. Штраф до 500 000 рублей.", category: .uk),
        "шпионаж": Article(code: "Ст. 276 УК РФ", title: "Шпионаж", fullText: "Передача сведений, составляющих государственную тайну. Лишение свободы от 10 до 20 лет.", category: .uk),
        "измена": Article(code: "Ст. 275 УК РФ", title: "Государственная измена", fullText: "Выдача государственной тайны иностранному государству. Лишение свободы от 12 до 20 лет.", category: .uk),
        "убийство": Article(code: "Ст. 105 УК РФ", title: "Убийство", fullText: "Умышленное причинение смерти другому человеку. Лишение свободы от 6 до 15 лет.", category: .uk),
        "кража": Article(code: "Ст. 158 УК РФ", title: "Кража", fullText: "Тайное хищение чужого имущества. Штраф до 80 000 рублей или лишение свободы до 2 лет.", category: .uk),
        "грабёж": Article(code: "Ст. 161 УК РФ", title: "Грабёж", fullText: "Открытое хищение чужого имущества. Лишение свободы до 4 лет.", category: .uk),
        "мошенничество": Article(code: "Ст. 159 УК РФ", title: "Мошенничество", fullText: "Хищение чужого имущества путём обмана. Штраф до 120 000 рублей или лишение свободы до 2 лет.", category: .uk),
        "вымогательство": Article(code: "Ст. 163 УК РФ", title: "Вымогательство", fullText: "Требование передачи имущества под угрозой насилия. Лишение свободы до 4 лет.", category: .uk),
        "терроризм": Article(code: "Ст. 205 УК РФ", title: "Террористический акт", fullText: "Совершение взрыва, поджога в целях устрашения населения. Лишение свободы от 10 до 20 лет.", category: .uk),
        "захват": Article(code: "Ст. 206 УК РФ", title: "Захват заложника", fullText: "Захват или удержание лица в качестве заложника. Лишение свободы до 15 лет.", category: .uk),
        "бандитизм": Article(code: "Ст. 209 УК РФ", title: "Бандитизм", fullText: "Создание устойчивой вооружённой группы. Лишение свободы до 15 лет.", category: .uk),
        "изнасилование": Article(code: "Ст. 131 УК РФ", title: "Изнасилование", fullText: "Половое сношение с применением насилия. Лишение свободы от 3 до 6 лет.", category: .uk),
        "похищение": Article(code: "Ст. 126 УК РФ", title: "Похищение человека", fullText: "Похищение человека. Лишение свободы до 5 лет.", category: .uk),
        "поджог": Article(code: "Ст. 167 УК РФ", title: "Умышленное уничтожение имущества", fullText: "Уничтожение чужого имущества. Лишение свободы до 2 лет.", category: .uk),
        "подделка": Article(code: "Ст. 327 УК РФ", title: "Подделка документов", fullText: "Подделка официального документа. Лишение свободы до 3 лет.", category: .uk),
        "шантаж": Article(code: "Ст. 163 УК РФ", title: "Шантаж", fullText: "Требование передачи имущества под угрозой распространения сведений. Лишение свободы до 4 лет.", category: .uk),
    ]
}
''')

# === 3. App/App.swift ===
write("App/App.swift", '''import SwiftUI

@main
struct SoUchastnikApp: App {
    var body: some Scene {
        WindowGroup {
            ContentView()
        }
    }
}
''')

# === 4. App/ContentView.swift ===
write("App/ContentView.swift", '''import SwiftUI

struct ContentView: View {
    @State private var text = ""
    @State private var currentWord = ""
    @State private var detectedArticle: Article? = nil

    let letters: [[String]] = [
        ["Й","Ц","У","К","Е","Н","Г","Ш","Щ","З","Х","Ъ"],
        ["Ф","Ы","В","А","П","Р","О","Л","Д","Ж","Э"],
        ["Я","Ч","С","М","И","Т","Ь","Б","Ю","Ё"]
    ]

    var body: some View {
        ZStack {
            Color(red: 0.1, green: 0.1, blue: 0.15).ignoresSafeArea()
            VStack(spacing: 16) {
                VStack(spacing: 4) {
                    Text("СоУчастник")
                        .font(.system(size: 32, weight: .heavy, design: .rounded))
                        .foregroundColor(.white)
                    Text("Умная клавиатура с базой статей РФ")
                        .font(.footnote).foregroundColor(.gray)
                }
                .padding(.top, 10)

                ScrollView {
                    Text(text.isEmpty ? "Начни печатать..." : text)
                        .foregroundColor(text.isEmpty ? .gray : .white)
                        .font(.system(size: 18))
                        .frame(maxWidth: .infinity, alignment: .leading)
                        .padding(12)
                }
                .frame(minHeight: 80, maxHeight: 120)
                .background(Color.white.opacity(0.08))
                .cornerRadius(12)

                HStack {
                    Button(action: { text = ""; currentWord = "" }) {
                        Label("Очистить", systemImage: "trash")
                            .font(.footnote).foregroundColor(.red.opacity(0.8))
                    }
                    Spacer()
                    Text("Статей в базе: \\(ArticleDatabase.dangerousWords.count)")
                        .font(.caption2).foregroundColor(.gray)
                }

                VStack(spacing: 6) {
                    HStack {
                        Text("Слово:").font(.caption).foregroundColor(.gray)
                        Text(currentWord.isEmpty ? "—" : currentWord.uppercased())
                            .font(.caption).bold().foregroundColor(.yellow)
                        Spacer()
                    }
                    ForEach(letters, id: \\.self) { row in
                        HStack(spacing: 4) {
                            ForEach(row, id: \\.self) { letter in
                                Button(action: { tapLetter(letter) }) {
                                    Text(letter)
                                        .font(.system(size: 18, weight: .medium))
                                        .foregroundColor(.white)
                                        .frame(maxWidth: .infinity)
                                        .frame(height: 44)
                                        .background(Color.white.opacity(0.12))
                                        .cornerRadius(6)
                                }
                            }
                        }
                    }
                    HStack(spacing: 6) {
                        Button(action: { text += " "; currentWord = "" }) {
                            Text("ПРОБЕЛ").frame(maxWidth: .infinity).frame(height: 44)
                                .background(Color.white.opacity(0.12)).cornerRadius(6)
                                .foregroundColor(.white)
                        }
                        Button(action: {
                            guard !text.isEmpty else { return }
                            text.removeLast()
                            if !currentWord.isEmpty { currentWord.removeLast() }
                        }) {
                            Image(systemName: "delete.left")
                                .frame(width: 60, height: 44)
                                .background(Color.white.opacity(0.12)).cornerRadius(6)
                                .foregroundColor(.white)
                        }
                    }
                }
                .padding(8)
                .background(Color.black.opacity(0.3))
                .cornerRadius(12)
                Spacer()
            }
            .padding()

            if let article = detectedArticle {
                articleOverlay(article: article)
            }
        }
    }

    func articleOverlay(article: Article) -> some View {
        ZStack {
            Color.black.opacity(0.85).ignoresSafeArea().onTapGesture { closeArticle() }
            VStack(alignment: .leading, spacing: 16) {
                HStack {
                    Text(article.category.rawValue)
                        .font(.caption).bold().foregroundColor(.white)
                        .padding(.horizontal, 10).padding(.vertical, 4)
                        .background(article.category == .koap ? Color.orange : Color.red)
                        .cornerRadius(6)
                    Spacer()
                    Text("⚠️").font(.title)
                }
                Text(article.code).font(.system(size: 24, weight: .heavy, design: .rounded)).foregroundColor(.white)
                Text(article.title).font(.headline).foregroundColor(article.category == .koap ? .orange : .red)
                Divider().background(Color.white.opacity(0.2))
                ScrollView {
                    Text(article.fullText)
                        .font(.system(size: 15)).foregroundColor(.white.opacity(0.9)).lineSpacing(4)
                }.frame(maxHeight: 200)
                HStack(spacing: 12) {
                    Button(action: {
                        text += "\\n---\\n\\(article.code): \\(article.fullText)\\n---\\n"
                        closeArticle()
                    }) {
                        Text("Вставить").font(.headline).foregroundColor(.white)
                            .frame(maxWidth: .infinity).padding(.vertical, 14)
                            .background(article.category == .koap ? Color.orange : Color.red)
                            .cornerRadius(10)
                    }
                    Button(action: { closeArticle() }) {
                        Text("Закрыть").font(.headline).foregroundColor(.white)
                            .frame(maxWidth: .infinity).padding(.vertical, 14)
                            .background(Color.white.opacity(0.15)).cornerRadius(10)
                    }
                }
            }
            .padding(24)
            .background(Color(red: 0.15, green: 0.15, blue: 0.2))
            .cornerRadius(20)
            .padding(.horizontal, 20)
        }
    }

    func tapLetter(_ letter: String) {
        text += letter.lowercased()
        currentWord += letter.lowercased()
        checkWord()
    }

    func checkWord() {
        let word = currentWord.lowercased()
        for (key, article) in ArticleDatabase.dangerousWords {
            if word == key || word.hasSuffix(key) {
                withAnimation(.spring(response: 0.3, dampingFraction: 0.7)) {
                    detectedArticle = article
                }
                currentWord = ""
                return
            }
        }
    }

    func closeArticle() {
        withAnimation { detectedArticle = nil }
    }
}
''')

# === 5. App/Info.plist ===
write("App/Info.plist", '''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleDevelopmentRegion</key>
    <string>ru</string>
    <key>CFBundleExecutable</key>
    <string>$(EXECUTABLE_NAME)</string>
    <key>CFBundleIdentifier</key>
    <string>$(PRODUCT_BUNDLE_IDENTIFIER)</string>
    <key>CFBundleInfoDictionaryVersion</key>
    <string>6.0</string>
    <key>CFBundleName</key>
    <string>$(PRODUCT_NAME)</string>
    <key>CFBundlePackageType</key>
    <string>APPL</string>
    <key>CFBundleShortVersionString</key>
    <string>1.0</string>
    <key>CFBundleVersion</key>
    <string>1</string>
</dict>
</plist>
''')

# === 6. Keyboard/KeyboardViewController.swift ===
write("Keyboard/KeyboardViewController.swift", '''import UIKit

class KeyboardViewController: UIInputViewController {

    private var currentWord = ""

    private let rows: [[String]] = [
        ["й","ц","у","к","е","н","г","ш","щ","з","х","ъ"],
        ["ф","ы","в","а","п","р","о","л","д","ж","э"],
        ["я","ч","с","м","и","т","ь","б","ю","ё"]
    ]

    override func viewDidLoad() {
        super.viewDidLoad()
        setupKeyboard()
    }

    private func setupKeyboard() {
        view.backgroundColor = UIColor(white: 0.15, alpha: 1)

        let mainStack = UIStackView()
        mainStack.axis = .vertical
        mainStack.spacing = 6
        mainStack.translatesAutoresizingMaskIntoConstraints = false
        view.addSubview(mainStack)

        NSLayoutConstraint.activate([
            mainStack.leadingAnchor.constraint(equalTo: view.leadingAnchor, constant: 4),
            mainStack.trailingAnchor.constraint(equalTo: view.trailingAnchor, constant: -4),
            mainStack.topAnchor.constraint(equalTo: view.topAnchor, constant: 6),
            mainStack.bottomAnchor.constraint(equalTo: view.bottomAnchor, constant: -6)
        ])

        for row in rows {
            let rowStack = UIStackView()
            rowStack.axis = .horizontal
            rowStack.spacing = 4
            rowStack.distribution = .fillEqually
            for letter in row {
                rowStack.addArrangedSubview(makeKey(title: letter.uppercased(), action: #selector(letterTapped(_:))))
            }
            mainStack.addArrangedSubview(rowStack)
        }

        let bottomStack = UIStackView()
        bottomStack.axis = .horizontal
        bottomStack.spacing = 4
        bottomStack.distribution = .fillEqually

        bottomStack.addArrangedSubview(makeKey(title: "🌐", action: #selector(nextKeyboard)))
        bottomStack.addArrangedSubview(makeKey(title: "Пробел", action: #selector(spaceTapped)))
        bottomStack.addArrangedSubview(makeKey(title: "⌫", action: #selector(deleteTapped)))
        mainStack.addArrangedSubview(bottomStack)
    }

    private func makeKey(title: String, action: Selector) -> UIButton {
        let btn = UIButton(type: .system)
        btn.setTitle(title, for: .normal)
        btn.titleLabel?.font = .systemFont(ofSize: 16, weight: .medium)
        btn.setTitleColor(.white, for: .normal)
        btn.backgroundColor = UIColor(white: 0.3, alpha: 1)
        btn.layer.cornerRadius = 5
        btn.addTarget(self, action: action, for: .touchUpInside)
        btn.heightAnchor.constraint(equalToConstant: 42).isActive = true
        return btn
    }

    @objc private func letterTapped(_ sender: UIButton) {
        guard let letter = sender.title(for: .normal)?.lowercased() else { return }
        textDocumentProxy.insertText(letter)
        currentWord += letter
        checkWord()
    }

    @objc private func spaceTapped() {
        textDocumentProxy.insertText(" ")
        currentWord = ""
    }

    @objc private func deleteTapped() {
        textDocumentProxy.deleteBackward()
        if !currentWord.isEmpty { currentWord.removeLast() }
    }

    @objc private func nextKeyboard() {
        advanceToNextInputMode()
    }

    private func checkWord() {
        let word = currentWord.lowercased()
        for (key, article) in ArticleDatabase.dangerousWords {
            if word == key || word.hasSuffix(key) {
                showArticle(article)
                currentWord = ""
                return
            }
        }
    }

    private func showArticle(_ article: Article) {
        let alert = UIAlertController(
            title: "\\(article.code) — \\(article.title)",
            message: article.fullText,
            preferredStyle: .alert
        )
        alert.addAction(UIAlertAction(title: "Вставить статью", style: .default) { [weak self] _ in
            self?.textDocumentProxy.insertText("\\n\\(article.code): \\(article.fullText)\\n")
        })
        alert.addAction(UIAlertAction(title: "Отмена", style: .cancel))
        present(alert, animated: true)
    }
}
''')

# === 7. Keyboard/Info.plist ===
write("Keyboard/Info.plist", '''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleDevelopmentRegion</key>
    <string>ru</string>
    <key>CFBundleExecutable</key>
    <string>$(EXECUTABLE_NAME)</string>
    <key>CFBundleIdentifier</key>
    <string>$(PRODUCT_BUNDLE_IDENTIFIER)</string>
    <key>CFBundleInfoDictionaryVersion</key>
    <string>6.0</string>
    <key>CFBundleName</key>
    <string>$(PRODUCT_NAME)</string>
    <key>CFBundlePackageType</key>
    <string>XPC!</string>
    <key>CFBundleShortVersionString</key>
    <string>1.0</string>
    <key>CFBundleVersion</key>
    <string>1</string>
    <key>NSExtension</key>
    <dict>
        <key>NSExtensionAttributes</key>
        <dict>
            <key>IsASCIICapable</key>
            <true/>
            <key>PrefersRightToLeft</key>
            <false/>
            <key>PrimaryLanguage</key>
            <string>ru</string>
            <key>RequestsOpenAccess</key>
            <false/>
        </dict>
        <key>NSExtensionPointIdentifier</key>
        <string>com.apple.keyboard-service</string>
        <key>NSExtensionPrincipalClass</key>
        <string>$(PRODUCT_MODULE_NAME).KeyboardViewController</string>
    </dict>
</dict>
</plist>
''')

# === 8. .github/workflows/build.yml ===
write(".github/workflows/build.yml", """name: Build iOS App

on:
  push:
    branches: [ main ]
  workflow_dispatch:

jobs:
  build:
    runs-on: macos-15

    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Install XcodeGen
        run: brew install xcodegen

      - name: Generate Xcode project
        run: xcodegen generate

      - name: Build archive (unsigned)
        run: |
          xcodebuild archive \\
            -project SoUchastnik.xcodeproj \\
            -scheme SoUchastnik \\
            -sdk iphoneos \\
            -configuration Release \\
            -archivePath $PWD/build/SoUchastnik.xcarchive \\
            CODE_SIGN_IDENTITY="" \\
            CODE_SIGNING_REQUIRED=NO \\
            CODE_SIGNING_ALLOWED=NO \\
            CODE_SIGN_ENTITLEMENTS=""

      - name: Package unsigned IPA
        run: |
          mkdir -p build/Payload
          cp -R build/SoUchastnik.xcarchive/Products/Applications/SoUchastnik.app build/Payload/
          cd build
          zip -r SoUchastnik-unsigned.ipa Payload
          ls -la

      - name: Upload IPA
        uses: actions/upload-artifact@v4
        with:
          name: SoUchastnik-unsigned-ipa
          path: build/SoUchastnik-unsigned.ipa
          retention-days: 30
""")

# === 9. .gitignore ===
write(".gitignore", """.build/
.crosscode/
*.ipa
*.dSYM
.DS_Store
xcuserdata/
*.xcuserstate
.swiftpm/
Package.resolved
build/
*.xcodeproj
""")

print("\\n✅ Все файлы созданы. Теперь: git add . && git commit -m 'Xcode project' && git push")