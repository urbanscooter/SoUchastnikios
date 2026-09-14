import UIKit

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
            title: "\(article.code) — \(article.title)",
            message: article.fullText,
            preferredStyle: .alert
        )
        alert.addAction(UIAlertAction(title: "Вставить статью", style: .default) { [weak self] _ in
            self?.textDocumentProxy.insertText("\n\(article.code): \(article.fullText)\n")
        })
        alert.addAction(UIAlertAction(title: "Отмена", style: .cancel))
        present(alert, animated: true)
    }
}
