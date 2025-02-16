//
//  DetailView.swift
//  pineapple WatchKit Extension
//
//  Created by Rohan Viswanathan on 2/13/25.
//

import SwiftUI

struct DetailView: View {
    // PROPERTY
    let task: Task
    let count: Int
    let index: Int
    
    
    // BODY
    
    var body: some View {
        VStack(alignment: .center, spacing: 3) {
            // HEADER
            HStack {
                Capsule()
                    .frame(height: 1)
                
                Image(systemName: "task.text")
                
                Capsule()
                    .frame(height: 1)
            } //: HSTACK
            .foregroundColor(.accentColor)
            
            // CONTENT
            Spacer()
            ScrollView(.vertical) {
                Text(task.text)
                    .font(.title3)
                    .fontWeight(.semibold)
                    .multilineTextAlignment(.center)
            }
            Spacer()
            
            // FOOTER
            HStack(alignment: .center) {
                Spacer()
                Text("\(index + 1) / \(count)")
                Spacer()
            } //. HSTACK
            .foregroundColor(.secondary)
        } //: VSTACK
        .padding(3)
    }
}

// PREVIEW

struct DetailView_Previews: PreviewProvider {
    static var sampleData: Task = Task(id: UUID(), text: "Hello, World")
    static var previews: some View {
        DetailView(task: sampleData, count: 5, index: 1)
    }
}
