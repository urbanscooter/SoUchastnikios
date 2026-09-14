import os

ROOT = os.getcwd()

def write(path, content):
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"✓ {path}")

# ============ 1. project.yml ============
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
            RequestsOpenAccess: true
    settings:
      base:
        PRODUCT_BUNDLE_IDENTIFIER: com.urbanscooter.souchastnik.keyboard
        MARKETING_VERSION: "1.0"
        CURRENT_PROJECT_VERSION: "1"
        CODE_SIGN_IDENTITY: ""
        CODE_SIGNING_REQUIRED: "NO"
        CODE_SIGNING_ALLOWED: "NO"
""")

# ============ 2. Shared/ArticleDatabase.swift ============
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
        "дискредитация": Article(code: "ст. 20.3.3 КоАП", title: "дискредитация ВС РФ · 30–50 тыс ₽", fullText: "Публичные действия, направленные на дискредитацию использования Вооруженных Сил Российской Федерации в целях защиты интересов РФ и ее граждан, поддержания международного мира и безопасности. Влечет наложение административного штрафа на граждан в размере от тридцати тысяч до пятидесяти тысяч рублей.", category: .koap),
        "фейк": Article(code: "ст. 13.15 КоАП", title: "фейки · 30–100 тыс ₽", fullText: "Распространение в средствах массовой информации, а также в информационно-телекоммуникационных сетях заведомо недостоверной общественно значимой информации под видом достоверных сообщений. Влечет наложение административного штрафа на граждан в размере от тридцати тысяч до ста тысяч рублей.", category: .koap),
        "хулиганство": Article(code: "ст. 20.1 КоАП", title: "мелкое хулиганство · 500–1000 ₽", fullText: "Мелкое хулиганство, то есть нарушение общественного порядка, выражающее явное неуважение к обществу, сопровождающееся нецензурной бранью в общественных местах. Влечет наложение административного штрафа в размере от пятисот до одной тысячи рублей или административный арест на срок до пятнадцати суток.", category: .koap),
        "митинг": Article(code: "ст. 20.2 КоАП", title: "нарушение правил митинга · 10–20 тыс ₽", fullText: "Нарушение организатором публичного мероприятия установленного порядка организации либо проведения собрания, митинга, демонстрации, шествия или пикетирования. Влечет наложение административного штрафа на граждан в размере от десяти тысяч до двадцати тысяч рублей или обязательные работы на срок до сорока часов.", category: .koap),
        "пикет": Article(code: "ст. 20.2 КоАП", title: "нарушение правил пикетирования · 10–20 тыс ₽", fullText: "Нарушение участником публичного мероприятия установленного порядка проведения собрания, митинга, демонстрации, шествия или пикетирования. Влечет наложение административного штрафа на граждан в размере от десяти тысяч до двадцати тысяч рублей.", category: .koap),
        "оскорбление": Article(code: "ст. 5.61 КоАП", title: "оскорбление · 1–3 тыс ₽", fullText: "Оскорбление, то есть унижение чести и достоинства другого лица, выраженное в неприличной форме. Влечет наложение административного штрафа на граждан в размере от одной тысячи до трех тысяч рублей.", category: .koap),
        "наркотик": Article(code: "ст. 6.8 КоАП", title: "незаконный оборот наркотиков · 4–5 тыс ₽", fullText: "Незаконные приобретение, хранение, перевозка, изготовление, переработка без цели сбыта наркотических средств. Влекут наложение административного штрафа в размере от четырех тысяч до пяти тысяч рублей или административный арест на срок до пятнадцати суток.", category: .koap),
        "пьяный": Article(code: "ст. 12.8 КоАП", title: "вождение в нетрезвом виде · 30 тыс ₽", fullText: "Управление транспортным средством водителем, находящимся в состоянии опьянения. Влечет наложение административного штрафа в размере тридцати тысяч рублей с лишением права управления транспортными средствами на срок от полутора до двух лет.", category: .koap),
        "скорость": Article(code: "ст. 12.9 КоАП", title: "превышение скорости · 500 ₽", fullText: "Превышение установленной скорости движения транспортного средства на величину более 20, но не более 40 километров в час. Влечет наложение административного штрафа в размере пятисот рублей.", category: .koap),
        "парковка": Article(code: "ст. 12.19 КоАП", title: "нарушение правил парковки · 500–5000 ₽", fullText: "Нарушение правил остановки и стоянки транспортных средств. Влечет предупреждение или наложение административного штрафа в размере от пятисот до пяти тысяч рублей.", category: .koap),
        "экстремизм": Article(code: "ст. 282 УК", title: "возбуждение ненависти · до 5 лет", fullText: "Действия, направленные на возбуждение ненависти либо вражды, а также на унижение достоинства человека либо группы лиц по признакам пола, расы, национальности, языка, происхождения, отношения к религии. Наказываются штрафом в размере от трехсот тысяч до пятисот тысяч рублей либо лишением свободы на срок от двух до пяти лет.", category: .uk),
        "взятка": Article(code: "ст. 291 УК", title: "дача взятки · до 8 лет", fullText: "Дача взятки должностному лицу, иностранному должностному лицу либо должностному лицу публичной международной организации лично или через посредника. Наказывается штрафом в размере до двухсот тысяч рублей или лишением свободы на срок до восьми лет.", category: .uk),
        "клевета": Article(code: "ст. 128.1 УК", title: "клевета · до 500 тыс ₽", fullText: "Клевета, то есть распространение заведомо ложных сведений, порочащих честь и достоинство другого лица или подрывающих его репутацию. Наказывается штрафом в размере до пятисот тысяч рублей.", category: .uk),
        "шпионаж": Article(code: "ст. 276 УК", title: "шпионаж · 10–20 лет", fullText: "Передача, собирание, похищение или хранение в целях передачи иностранному государству сведений, составляющих государственную тайну. Наказываются лишением свободы на срок от десяти до двадцати лет.", category: .uk),
        "измена": Article(code: "ст. 275 УК", title: "государственная измена · 12–20 лет", fullText: "Государственная измена, то есть совершенные гражданином Российской Федерации шпионаж, выдача иностранному государству сведений, составляющих государственную тайну. Наказывается лишением свободы на срок от двенадцати до двадцати лет.", category: .uk),
        "убийство": Article(code: "ст. 105 УК", title: "убийство · 6–15 лет", fullText: "Убийство, то есть умышленное причинение смерти другому человеку. Наказывается лишением свободы на срок от шести до пятнадцати лет с ограничением свободы на срок до двух лет.", category: .uk),
        "кража": Article(code: "ст. 158 УК", title: "кража · до 2 лет", fullText: "Кража, то есть тайное хищение чужого имущества. Наказывается штрафом в размере до восьмидесяти тысяч рублей либо лишением свободы на срок до двух лет.", category: .uk),
        "грабёж": Article(code: "ст. 161 УК", title: "грабёж · до 4 лет", fullText: "Грабеж, то есть открытое хищение чужого имущества. Наказывается лишением свободы на срок до четырех лет.", category: .uk),
        "мошенничество": Article(code: "ст. 159 УК", title: "мошенничество · до 2 лет", fullText: "Мошенничество, то есть хищение чужого имущества путем обмана или злоупотребления доверием. Наказывается штрафом в размере до ста двадцати тысяч рублей либо лишением свободы на срок до двух лет.", category: .uk),
        "вымогательство": Article(code: "ст. 163 УК", title: "вымогательство · до 4 лет", fullText: "Вымогательство, то есть требование передачи чужого имущества под угрозой применения насилия либо уничтожения или повреждения чужого имущества. Наказывается лишением свободы на срок до четырех лет.", category: .uk),
        "терроризм": Article(code: "ст. 205 УК", title: "террористический акт · 10–20 лет", fullText: "Совершение взрыва, поджога или иных действий, устрашающих население и создающих опасность гибели человека. Наказываются лишением свободы на срок от десяти до двадцати лет.", category: .uk),
        "захват": Article(code: "ст. 206 УК", title: "захват заложника · до 15 лет", fullText: "Захват или удержание лица в качестве заложника, совершенные в целях понуждения государства, организации или гражданина совершить какое-либо действие. Наказываются лишением свободы на срок до пятнадцати лет.", category: .uk),
        "бандитизм": Article(code: "ст. 209 УК", title: "бандитизм · до 15 лет", fullText: "Создание устойчивой вооруженной группы (банды) в целях нападения на граждан или организации, а равно руководство такой группой. Наказывается лишением свободы на срок до пятнадцати лет.", category: .uk),
        "похищение": Article(code: "ст. 126 УК", title: "похищение человека · до 5 лет", fullText: "Похищение человека. Наказывается принудительными работами на срок до пяти лет либо лишением свободы на тот же срок.", category: .uk),
        "поджог": Article(code: "ст. 167 УК", title: "умышленное уничтожение имущества · до 2 лет", fullText: "Умышленное уничтожение или повреждение чужого имущества, если эти деяния повлекли причинение значительного ущерба. Наказываются лишением свободы на срок до двух лет.", category: .uk),
        "подделка": Article(code: "ст. 327 УК", title: "подделка документов · до 3 лет", fullText: "Подделка официального документа, предоставляющего права или освобождающего от обязанностей, в целях его использования. Наказывается лишением свободы на срок до трех лет.", category: .uk),
        "шантаж": Article(code: "ст. 163 УК", title: "шантаж · до 4 лет", fullText: "Вымогательство под угрозой распространения сведений, позорящих потерпевшего или его близких. Наказывается лишением свободы на срок до четырех лет.", category: .uk),
        "изнасилование": Article(code: "ст. 131 УК", title: "изнасилование · 3–6 лет", fullText: "Изнасилование, то есть половое сношение с применением насилия или с угрозой его применения. Наказывается лишением свободы на срок от трех до шести лет.", category: .uk),
    ]
}
''')

# ============ 3. App/App.swift ============
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

# ============ 4. App/ContentView.swift ============
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

# ============ 5. App/Info.plist ============
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

# ============ 6. Keyboard/KeyboardViewController.swift ============
write("Keyboard/KeyboardViewController.swift", '''import UIKit

class KeyboardViewController: UIInputViewController {

    private var currentWord = ""
    private var isUppercase = false
    private var isNumbersLayer = false

    private var bannerView: UIView!
    private var bannerLabel: UILabel!
    private var keysStack: UIStackView!
    private var currentArticle: Article?

    private let lettersRows: [[String]] = [
        ["й","ц","у","к","е","н","г","ш","щ","з","х","ъ"],
        ["ф","ы","в","а","п","р","о","л","д","ж","э"],
        ["я","ч","с","м","и","т","ь","б","ю","ё"]
    ]

    private let numbersRows: [[String]] = [
        ["1","2","3","4","5","6","7","8","9","0"],
        ["-","/",":",";","(",")","₽","&","@","\\""],
        [".",",","?","!","'","*","#","%","+","="]
    ]

    override func viewDidLoad() {
        super.viewDidLoad()
        setupUI()
    }

    private func setupUI() {
        view.backgroundColor = UIColor(white: 0.12, alpha: 1)

        let mainStack = UIStackView()
        mainStack.axis = .vertical
        mainStack.spacing = 5
        mainStack.translatesAutoresizingMaskIntoConstraints = false
        view.addSubview(mainStack)

        NSLayoutConstraint.activate([
            mainStack.leadingAnchor.constraint(equalTo: view.leadingAnchor, constant: 3),
            mainStack.trailingAnchor.constraint(equalTo: view.trailingAnchor, constant: -3),
            mainStack.topAnchor.constraint(equalTo: view.topAnchor, constant: 5),
            mainStack.bottomAnchor.constraint(equalTo: view.bottomAnchor, constant: -5)
        ])

        setupBanner(in: mainStack)

        keysStack = UIStackView()
        keysStack.axis = .vertical
        keysStack.spacing = 5
        keysStack.distribution = .fillEqually
        mainStack.addArrangedSubview(keysStack)

        rebuildKeys()
    }

    private func setupBanner(in parent: UIStackView) {
        bannerView = UIView()
        bannerView.backgroundColor = UIColor(red: 0.16, green: 0.16, blue: 0.20, alpha: 1)
        bannerView.layer.cornerRadius = 8
        bannerView.isHidden = true
        bannerView.translatesAutoresizingMaskIntoConstraints = false
        bannerView.heightAnchor.constraint(equalToConstant: 34).isActive = true

        let tap = UITapGestureRecognizer(target: self, action: #selector(bannerTapped))
        bannerView.addGestureRecognizer(tap)
        bannerView.isUserInteractionEnabled = true

        bannerLabel = UILabel()
        bannerLabel.font = .systemFont(ofSize: 13, weight: .medium)
        bannerLabel.textColor = UIColor(red: 1.0, green: 0.58, blue: 0.30, alpha: 1)
        bannerLabel.numberOfLines = 1
        bannerLabel.adjustsFontSizeToFitWidth = true
        bannerLabel.minimumScaleFactor = 0.7
        bannerLabel.translatesAutoresizingMaskIntoConstraints = false

        let dot = UIView()
        dot.backgroundColor = UIColor(red: 1.0, green: 0.58, blue: 0.30, alpha: 1)
        dot.layer.cornerRadius = 4
        dot.translatesAutoresizingMaskIntoConstraints = false

        bannerView.addSubview(bannerLabel)
        bannerView.addSubview(dot)

        NSLayoutConstraint.activate([
            bannerLabel.leadingAnchor.constraint(equalTo: bannerView.leadingAnchor, constant: 12),
            bannerLabel.trailingAnchor.constraint(equalTo: dot.leadingAnchor, constant: -8),
            bannerLabel.centerYAnchor.constraint(equalTo: bannerView.centerYAnchor),

            dot.trailingAnchor.constraint(equalTo: bannerView.trailingAnchor, constant: -12),
            dot.centerYAnchor.constraint(equalTo: bannerView.centerYAnchor),
            dot.widthAnchor.constraint(equalToConstant: 8),
            dot.heightAnchor.constraint(equalToConstant: 8)
        ])

        parent.addArrangedSubview(bannerView)
    }

    private func rebuildKeys() {
        keysStack.arrangedSubviews.forEach { $0.removeFromSuperview() }

        let rows = isNumbersLayer ? numbersRows : lettersRows

        keysStack.addArrangedSubview(makeRow(keys: rows[0].map { (key: $0, title: displayTitle($0)) }))
        keysStack.addArrangedSubview(makeRow(keys: rows[1].map { (key: $0, title: displayTitle($0)) }))

        var row3Keys: [(key: String, title: String)] = []
        row3Keys.append((key: "shift", title: "⇧"))
        for ch in rows[2] {
            row3Keys.append((key: ch, title: displayTitle(ch)))
        }
        row3Keys.append((key: "delete", title: "⌫"))
        keysStack.addArrangedSubview(makeRow(keys: row3Keys, wideKeys: ["shift", "delete"]))

        let row4 = UIStackView()
        row4.axis = .horizontal
        row4.spacing = 5
        row4.distribution = .fill

        let numbersBtn = makeButton(key: "numbers", title: isNumbersLayer ? "АБВ" : "?123")
        numbersBtn.widthAnchor.constraint(equalToConstant: 58).isActive = true

        let langBtn = makeButton(key: "lang", title: "RU")
        langBtn.widthAnchor.constraint(equalToConstant: 48).isActive = true

        let spaceBtn = makeButton(key: "space", title: "пробел")

        let dotBtn = makeButton(key: "dot", title: ".")
        dotBtn.widthAnchor.constraint(equalToConstant: 48).isActive = true

        let returnBtn = makeButton(key: "return", title: "↵")
        returnBtn.backgroundColor = UIColor(red: 0.18, green: 0.48, blue: 0.92, alpha: 1)
        returnBtn.widthAnchor.constraint(equalToConstant: 64).isActive = true

        row4.addArrangedSubview(numbersBtn)
        row4.addArrangedSubview(langBtn)
        row4.addArrangedSubview(spaceBtn)
        row4.addArrangedSubview(dotBtn)
        row4.addArrangedSubview(returnBtn)
        keysStack.addArrangedSubview(row4)
    }

    private func displayTitle(_ ch: String) -> String {
        if isUppercase && !isNumbersLayer && ch.count == 1 && ch.first!.isLetter {
            return ch.uppercased()
        }
        return ch
    }

    private func makeRow(keys: [(key: String, title: String)], wideKeys: [String] = []) -> UIStackView {
        let stack = UIStackView()
        stack.axis = .horizontal
        stack.spacing = 5
        stack.distribution = .fill

        for (key, title) in keys {
            let btn = makeButton(key: key, title: title)
            if wideKeys.contains(key) {
                btn.widthAnchor.constraint(equalToConstant: 46).isActive = true
            }
            stack.addArrangedSubview(btn)
        }
        return stack
    }

    private func makeButton(key: String, title: String) -> UIButton {
        let btn = UIButton(type: .system)
        btn.setTitle(title, for: .normal)
        btn.titleLabel?.font = .systemFont(ofSize: 20, weight: .regular)
        btn.setTitleColor(.white, for: .normal)
        btn.accessibilityIdentifier = key

        switch key {
        case "shift", "delete", "numbers", "lang":
            btn.backgroundColor = UIColor(white: 0.25, alpha: 1)
        case "return":
            btn.backgroundColor = UIColor(red: 0.18, green: 0.48, blue: 0.92, alpha: 1)
        default:
            btn.backgroundColor = UIColor(white: 0.36, alpha: 1)
        }

        btn.layer.cornerRadius = 6
        btn.heightAnchor.constraint(equalToConstant: 42).isActive = true
        btn.addTarget(self, action: #selector(keyPressed(_:)), for: .touchUpInside)
        return btn
    }

    @objc private func keyPressed(_ sender: UIButton) {
        guard let key = sender.accessibilityIdentifier else { return }

        switch key {
        case "shift":
            isUppercase.toggle()
            rebuildKeys()
            return
        case "delete":
            textDocumentProxy.deleteBackward()
            if !currentWord.isEmpty { currentWord.removeLast() }
            return
        case "numbers":
            isNumbersLayer.toggle()
            isUppercase = false
            rebuildKeys()
            return
        case "lang":
            advanceToNextInputMode()
            return
        case "space":
            textDocumentProxy.insertText(" ")
            currentWord = ""
            return
        case "dot":
            textDocumentProxy.insertText(".")
            return
        case "return":
            textDocumentProxy.insertText("\\n")
            currentWord = ""
            return
        default:
            break
        }

        var ch = key
        if isUppercase && !isNumbersLayer { ch = ch.uppercased() }
        textDocumentProxy.insertText(ch)
        currentWord += ch.lowercased()

        if isUppercase && !isNumbersLayer {
            isUppercase = false
            rebuildKeys()
        }

        checkWord()
    }

    private func checkWord() {
        let word = currentWord.lowercased()
        for (trigger, article) in ArticleDatabase.dangerousWords {
            if word == trigger || (word.count >= trigger.count && word.hasSuffix(trigger)) {
                showBanner(article: article)
                currentWord = ""
                return
            }
        }
    }

    private func showBanner(article: Article) {
        currentArticle = article
        bannerLabel.text = "\\(article.code) · \\(article.title)"
        bannerView.isHidden = false
        bannerView.alpha = 0
        UIView.animate(withDuration: 0.2) {
            self.bannerView.alpha = 1
        }
    }

    private func hideBanner() {
        currentArticle = nil
        UIView.animate(withDuration: 0.15, animations: {
            self.bannerView.alpha = 0
        }, completion: { _ in
            self.bannerView.isHidden = true
            self.bannerView.alpha = 1
        })
    }

    @objc private func bannerTapped() {
        guard let article = currentArticle else { return }
        let text = "\\n\\(article.code) — \\(article.title)\\n\\(article.fullText)\\n"
        textDocumentProxy.insertText(text)
        hideBanner()
    }
}
''')

# ============ 7. Keyboard/Info.plist ============
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
            <true/>
        </dict>
        <key>NSExtensionPointIdentifier</key>
        <string>com.apple.keyboard-service</string>
        <key>NSExtensionPrincipalClass</key>
        <string>$(PRODUCT_MODULE_NAME).KeyboardViewController</string>
    </dict>
</dict>
</plist>
''')

# ============ 8. .github/workflows/build.yml ============
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

# ============ 9. .gitignore ============
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

print("\\n✅ Всё создано. Дальше:")
print("   git add .")
print("   git commit -m 'Fix keyboard layout + banner'")
print("   git push")