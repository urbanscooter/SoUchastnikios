import UIKit

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
        ["-","/",":",";","(",")","₽","&","@","\""],
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
            textDocumentProxy.insertText("\n")
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
        bannerLabel.text = "\(article.code) · \(article.title)"
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
        let text = "\n\(article.code) — \(article.title)\n\(article.fullText)\n"
        textDocumentProxy.insertText(text)
        hideBanner()
    }
}
