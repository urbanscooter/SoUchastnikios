import SwiftUI

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
                    Text("Статей в базе: \(ArticleDatabase.dangerousWords.count)")
                        .font(.caption2).foregroundColor(.gray)
                }

                VStack(spacing: 6) {
                    HStack {
                        Text("Слово:").font(.caption).foregroundColor(.gray)
                        Text(currentWord.isEmpty ? "—" : currentWord.uppercased())
                            .font(.caption).bold().foregroundColor(.yellow)
                        Spacer()
                    }
                    ForEach(letters, id: \.self) { row in
                        HStack(spacing: 4) {
                            ForEach(row, id: \.self) { letter in
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
                        text += "\n---\n\(article.code): \(article.fullText)\n---\n"
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
