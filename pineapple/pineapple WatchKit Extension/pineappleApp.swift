//
//  pineappleApp.swift
//  pineapple WatchKit Extension
//
//  Created by Rohan Viswanathan on 2/13/25.
//

import SwiftUI

@main
struct pineappleApp: App {
    @SceneBuilder var body: some Scene {
        WindowGroup {
            NavigationView {
                ContentView()
            }
        }

        WKNotificationScene(controller: NotificationController.self, category: "myCategory")
    }
}
