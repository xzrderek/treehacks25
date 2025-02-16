//
//  ContentView.swift
//  pineapple WatchKit Extension
//
//  Created by Rohan Viswanathan on 2/13/25.
//

import SwiftUI

struct ContentView: View {
    // PROPERTY
    @State private var tasks: [Task] = [Task]()
    @State private var text: String = ""
    // Add server URL configuration
    private let serverURL = Bundle.main.object(forInfoDictionaryKey: "ServerURL") as? String ?? "http://localhost:8000"
    
    // FUNCTION
    
    func save() {
        do {
            let data = try JSONEncoder().encode(tasks)
            let url = getDocumentDirectory().appendingPathComponent("tasks")
            try data.write(to: url)
        } catch {
            print("Saving data has failed!")
        }
    }
    
    func load() {
        DispatchQueue.main.async {
            do {
                let url = getDocumentDirectory().appendingPathComponent("tasks")
                let data = try Data(contentsOf: url)
                tasks = try JSONDecoder().decode([Task].self, from: data)
            } catch {
                // Do nothing
            }
        }
    }
    
    /// Deletes tasks using deletion offsets from the reversed list.
    func deleteFromReversed(offsets: IndexSet) {
        // Map the reversed offsets back to the original array indexes.
        let mappedOffsets = offsets.map { tasks.count - 1 - $0 }.sorted()
        withAnimation {
            tasks.remove(atOffsets: IndexSet(mappedOffsets))
            save()
        }
    }
    
    func getDocumentDirectory() -> URL {
        FileManager.default.urls(for: .documentDirectory, in: .userDomainMask)[0]
    }
    
    // BODY
    var body: some View {
        VStack {
            HStack(alignment: .center, spacing: 6) {
                TextField("Add New Task", text: $text)
                Button {
                    guard text.isEmpty == false else { return }
                    let task = Task(id: UUID(), text: text)
                    tasks.append(task)
                    text = ""
                    save()
                } label: {
                    Image(systemName: "plus.circle")
                        .font(.system(size: 42, weight: .semibold))
                }
                .fixedSize()
                .buttonStyle(PlainButtonStyle())
                .foregroundColor(.accentColor)
            } //: HSTACK
            
            Spacer()
            
            if tasks.count >= 1 {
                List {
                    ForEach((0..<tasks.count).reversed(), id: \.self) { i in
                        NavigationLink(destination: DetailView(task: tasks[i], count: tasks.count, index: i)) {
                            HStack {
                                Capsule()
                                    .frame(width: 4)
                                    .foregroundColor(.accentColor)
                                Text(tasks[i].text)
                                    .lineLimit(1)
                                    .padding(.leading, 5)
                            }
                        }
                    }
                    .onDelete(perform: deleteFromReversed)
                }
            } else {
                Spacer()
                Image(systemName: "note.text")
                    .resizable()
                    .scaledToFit()
                    .foregroundColor(.gray)
                    .opacity(0.25)
                    .padding(25)
                Spacer()
            }
        } //: VSTACK
        .navigationBarTitleDisplayMode(.inline)
        .onAppear(perform: load)
        // Overlay button remains unchanged.
        .overlay(
            Button {
                for task in tasks {
                    print("Task: \(task)")
                    guard let url = URL(string: "\(serverURL)/tasks/submit") else {
                        print("Invalid URL")
                        continue
                    }
                    
                    var request = URLRequest(url: url)
                    request.httpMethod = "POST"
                    request.addValue("application/json", forHTTPHeaderField: "Content-Type")
                    
                    let json: [String: String] = ["query": task.text]
                    do {
                        let jsonData = try JSONSerialization.data(withJSONObject: json)
                        request.httpBody = jsonData
                    } catch {
                        print("Error serializing JSON for task: \(task.text) - \(error)")
                        continue
                    }
                    
                    URLSession.shared.dataTask(with: request) { data, response, error in
                        if let error = error {
                            print("Error sending task \(task.text): \(error.localizedDescription)")
                        } else {
                            print("Successfully sent task: \(task.text)")
                        }
                        DispatchQueue.main.async {
                            if let index = tasks.firstIndex(where: { $0.id == task.id }) {
                                self.deleteFromReversed(offsets: IndexSet(integer: tasks.count - 1 - index))
                            }
                        }
                    }.resume()
                }
            } label: {
                Image(systemName: "arrowshape.turn.up.right")
                    .font(.system(size: 20, weight: .semibold))
                    .foregroundColor(.accentColor)
                    .padding(12)
                    .background(
                        Circle()
                            .fill(Color.white.opacity(0.6))
                    )
            }
            .buttonStyle(PlainButtonStyle())
            .padding(.bottom, 0.5)
            .padding(.trailing, 2)
            , alignment: .bottomTrailing
        )
    }
}

struct ContentView_Previews: PreviewProvider {
    static var previews: some View {
        ContentView()
    }
}
