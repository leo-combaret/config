import ApplicationServices
import Cocoa

private let zedBundleIdentifier = "dev.zed.Zed"
private let homeDirectory = FileManager.default.homeDirectoryForCurrentUser.path

private struct ProjectSpec {
    let name: String
    let path: String
    let backgroundColor: NSColor
    let foregroundColor: NSColor
}

private struct OnScreenWindow {
    let pid: pid_t
    let frame: CGRect
}

private let projects: [ProjectSpec] = [
    ProjectSpec(
        name: "dashboard",
        path: "\(homeDirectory)/mistral/dashboard",
        backgroundColor: NSColor(calibratedRed: 0.92, green: 0.12, blue: 0.16, alpha: 0.34),
        foregroundColor: NSColor(calibratedWhite: 1.0, alpha: 0.82)
    ),
    ProjectSpec(
        name: "seattle",
        path: "\(homeDirectory)/mistral/seattle",
        backgroundColor: NSColor(calibratedRed: 0.12, green: 0.38, blue: 0.95, alpha: 0.34),
        foregroundColor: NSColor(calibratedWhite: 1.0, alpha: 0.82)
    ),
    ProjectSpec(
        name: "budapest",
        path: "\(homeDirectory)/mistral/budapest",
        backgroundColor: NSColor(calibratedRed: 0.12, green: 0.62, blue: 0.28, alpha: 0.34),
        foregroundColor: NSColor(calibratedWhite: 1.0, alpha: 0.82)
    ),
    ProjectSpec(
        name: "dakar",
        path: "\(homeDirectory)/mistral/dakar",
        backgroundColor: NSColor(calibratedRed: 1.0, green: 0.82, blue: 0.08, alpha: 0.32),
        foregroundColor: NSColor(calibratedWhite: 1.0, alpha: 0.78)
    )
]

private final class PillView: NSView {
    private let label: NSTextField
    private var fillColor = NSColor(calibratedWhite: 0.0, alpha: 0.12)

    init(name: String) {
        label = NSTextField(labelWithString: name)
        super.init(frame: .zero)

        wantsLayer = true
        translatesAutoresizingMaskIntoConstraints = false

        label.font = NSFont.systemFont(ofSize: 12, weight: .medium)
        label.alignment = .center
        label.lineBreakMode = .byClipping
        label.textColor = NSColor(calibratedWhite: 1.0, alpha: 0.54)
        label.translatesAutoresizingMaskIntoConstraints = false

        addSubview(label)

        NSLayoutConstraint.activate([
            heightAnchor.constraint(equalToConstant: 26),
            widthAnchor.constraint(greaterThanOrEqualToConstant: max(58, label.intrinsicContentSize.width + 20)),
            label.leadingAnchor.constraint(equalTo: leadingAnchor, constant: 10),
            label.trailingAnchor.constraint(equalTo: trailingAnchor, constant: -10),
            label.centerYAnchor.constraint(equalTo: centerYAnchor)
        ])
    }

    @available(*, unavailable)
    required init?(coder: NSCoder) {
        fatalError("init(coder:) has not been implemented")
    }

    override var intrinsicContentSize: NSSize {
        NSSize(width: max(58, label.intrinsicContentSize.width + 20), height: 26)
    }

    override func draw(_ dirtyRect: NSRect) {
        super.draw(dirtyRect)
        fillColor.setFill()
        NSBezierPath(roundedRect: bounds, xRadius: 8, yRadius: 8).fill()
    }

    func setProject(_ project: ProjectSpec, active: Bool) {
        if active {
            fillColor = project.backgroundColor
            label.textColor = project.foregroundColor
        } else {
            fillColor = NSColor(calibratedWhite: 0.0, alpha: 0.12)
            label.textColor = NSColor(calibratedWhite: 1.0, alpha: 0.54)
        }
        needsDisplay = true
    }
}

private final class OverlayView: NSView {
    private let pillViews: [PillView]

    init() {
        pillViews = projects.map { PillView(name: $0.name) }
        super.init(frame: NSRect(x: 0, y: 0, width: 390, height: 38))

        wantsLayer = true
        layer?.backgroundColor = NSColor.clear.cgColor

        let stackView = NSStackView(views: pillViews)
        stackView.orientation = .horizontal
        stackView.alignment = .centerY
        stackView.spacing = 6
        stackView.translatesAutoresizingMaskIntoConstraints = false

        addSubview(stackView)

        NSLayoutConstraint.activate([
            stackView.centerXAnchor.constraint(equalTo: centerXAnchor),
            stackView.centerYAnchor.constraint(equalTo: centerYAnchor),
            stackView.leadingAnchor.constraint(greaterThanOrEqualTo: leadingAnchor, constant: 6),
            stackView.trailingAnchor.constraint(lessThanOrEqualTo: trailingAnchor, constant: -6)
        ])

        setActiveProject(nil)
    }

    @available(*, unavailable)
    required init?(coder: NSCoder) {
        fatalError("init(coder:) has not been implemented")
    }

    func setActiveProject(_ activeProject: ProjectSpec?) {
        for (index, project) in projects.enumerated() {
            pillViews[index].setProject(project, active: project.name == activeProject?.name)
        }
    }
}

private final class OverlayController: NSObject, NSApplicationDelegate {
    private let overlayView = OverlayView()
    private lazy var panel: NSPanel = {
        let panel = NSPanel(
            contentRect: NSRect(x: 0, y: 0, width: 390, height: 38),
            styleMask: [.borderless, .nonactivatingPanel],
            backing: .buffered,
            defer: false
        )
        panel.backgroundColor = .clear
        panel.collectionBehavior = [.canJoinAllSpaces, .fullScreenAuxiliary, .ignoresCycle]
        panel.contentView = overlayView
        panel.hasShadow = false
        panel.hidesOnDeactivate = false
        panel.ignoresMouseEvents = true
        panel.isMovable = false
        panel.isOpaque = false
        panel.level = .statusBar
        return panel
    }()

    private var timer: Timer?
    func applicationDidFinishLaunching(_ notification: Notification) {
        NSApp.setActivationPolicy(.accessory)
        requestAccessibilityIfNeeded()
        if !AXIsProcessTrusted() {
            print("zed-project-overlay requires Accessibility permission.")
            fflush(stdout)
        }

        timer = Timer.scheduledTimer(withTimeInterval: 0.2, repeats: true) { [weak self] _ in
            self?.refresh()
        }
        RunLoop.main.add(timer!, forMode: .common)
        refresh()
    }

    private func requestAccessibilityIfNeeded() {
        let options = [kAXTrustedCheckOptionPrompt.takeUnretainedValue() as String: true] as CFDictionary
        _ = AXIsProcessTrustedWithOptions(options)
    }

    private func refresh() {
        guard AXIsProcessTrusted() else {
            hide()
            return
        }

        guard let zedApplication = NSRunningApplication.runningApplications(withBundleIdentifier: zedBundleIdentifier).first else {
            hide()
            return
        }

        let zedIsFrontmost = NSWorkspace.shared.frontmostApplication?.bundleIdentifier == zedBundleIdentifier

        if zedIsFrontmost {
            if !showFrontZedWindow(for: zedApplication.processIdentifier) {
                showVisibleTargetZedWindow(for: zedApplication.processIdentifier)
            }
        } else {
            showVisibleTargetZedWindow(for: zedApplication.processIdentifier)
        }
    }

    private func showFrontZedWindow(for pid: pid_t) -> Bool {
        guard let window = frontWindow(for: pid) else {
            return false
        }

        guard isStandardWindow(window) else {
            return false
        }

        guard let frame = windowFrame(window) else {
            return false
        }

        guard let activeProject = activeProject(for: window) else {
            return false
        }

        overlayView.setActiveProject(activeProject)
        movePanel(toTopCenterOf: frame)

        if !panel.isVisible {
            panel.orderFrontRegardless()
        }
        return true
    }

    private func showVisibleTargetZedWindow(for pid: pid_t) {
        let visibleFrames = visibleZedWindowFrames(for: pid)

        guard !visibleFrames.isEmpty else {
            hide()
            return
        }

        let appElement = AXUIElementCreateApplication(pid)
        let windows = axElements(appElement, kAXWindowsAttribute as String) ?? []

        for window in windows {
            guard
                isStandardWindow(window),
                let frame = windowFrame(window),
                visibleFrames.contains(where: { approximatelySameFrame($0, frame) }),
                isWindowTopOnItsScreen(frame, pid: pid),
                let project = activeProject(for: window)
            else {
                continue
            }

            overlayView.setActiveProject(project)
            movePanel(toTopCenterOf: frame)

            if !panel.isVisible {
                panel.orderFrontRegardless()
            }
            return
        }

        hide()
    }

    private func isWindowTopOnItsScreen(_ frame: CGRect, pid: pid_t) -> Bool {
        let windows = orderedOnScreenWindows()

        guard
            let targetIndex = windows.firstIndex(where: { $0.pid == pid && approximatelySameFrame($0.frame, frame) }),
            let targetScreenFrame = screenFrame(containingMostOf: frame)
        else {
            return false
        }

        for window in windows[..<targetIndex] where intersects(window.frame, targetScreenFrame) {
            return false
        }

        return true
    }

    private func hide() {
        if panel.isVisible {
            panel.orderOut(nil)
        }
    }

    private func movePanel(toTopCenterOf windowFrame: CGRect) {
        let overlaySize = panel.frame.size
        let quartzOrigin = CGPoint(
            x: round(windowFrame.midX - overlaySize.width / 2),
            y: round(windowFrame.minY - 2)
        )
        let origin = appKitOrigin(forQuartzOrigin: quartzOrigin, size: overlaySize)

        panel.setFrame(NSRect(origin: origin, size: overlaySize), display: true)
    }

    private func appKitOrigin(forQuartzOrigin quartzOrigin: CGPoint, size: CGSize) -> CGPoint {
        let mainScreenMaxY = NSScreen.screens.first?.frame.maxY ?? 0
        return CGPoint(
            x: quartzOrigin.x,
            y: round(mainScreenMaxY - quartzOrigin.y - size.height)
        )
    }

    private func activeProject(for window: AXUIElement) -> ProjectSpec? {
        let documentPath = normalizedDocumentPath(axString(window, kAXDocumentAttribute as String))
        let title = (axString(window, kAXTitleAttribute as String) ?? "").lowercased()

        if let documentPath {
            for project in projects where documentPath == project.path || documentPath.hasPrefix(project.path + "/") {
                return project
            }
        }

        return projects.first { project in
            title.contains(project.name)
        }
    }

    private func normalizedDocumentPath(_ document: String?) -> String? {
        guard let document, !document.isEmpty else {
            return nil
        }

        if document.hasPrefix("file://") {
            return URL(string: document)?.standardizedFileURL.path
        }

        return NSString(string: document).standardizingPath
    }

    private func frontWindow(for pid: pid_t) -> AXUIElement? {
        let appElement = AXUIElementCreateApplication(pid)

        return axElements(appElement, kAXWindowsAttribute as String)?.first
    }

    private func orderedOnScreenWindows() -> [OnScreenWindow] {
        guard let windowInfo = CGWindowListCopyWindowInfo([.optionOnScreenOnly], kCGNullWindowID) as? [[String: Any]] else {
            return []
        }

        return windowInfo.compactMap { info in
            guard
                let pid = info[kCGWindowOwnerPID as String] as? pid_t,
                (info[kCGWindowLayer as String] as? Int) == 0,
                let bounds = info[kCGWindowBounds as String] as? [String: Any],
                let x = cgFloat(bounds["X"]),
                let y = cgFloat(bounds["Y"]),
                let width = cgFloat(bounds["Width"]),
                let height = cgFloat(bounds["Height"]),
                width > 80,
                height > 80
            else {
                return nil
            }

            return OnScreenWindow(pid: pid, frame: CGRect(x: x, y: y, width: width, height: height))
        }
    }

    private func visibleZedWindowFrames(for pid: pid_t) -> [CGRect] {
        orderedOnScreenWindows()
            .filter { $0.pid == pid && $0.frame.width > 300 && $0.frame.height > 200 }
            .map(\.frame)
    }

    private func approximatelySameFrame(_ lhs: CGRect, _ rhs: CGRect) -> Bool {
        abs(lhs.origin.x - rhs.origin.x) <= 8 &&
            abs(lhs.origin.y - rhs.origin.y) <= 8 &&
            abs(lhs.size.width - rhs.size.width) <= 8 &&
            abs(lhs.size.height - rhs.size.height) <= 8
    }

    private func screenFrame(containingMostOf frame: CGRect) -> CGRect? {
        let mainScreenMaxY = NSScreen.screens.first?.frame.maxY ?? 0

        return NSScreen.screens
            .map { screen -> CGRect in
                CGRect(
                    x: screen.frame.minX,
                    y: mainScreenMaxY - screen.frame.maxY,
                    width: screen.frame.width,
                    height: screen.frame.height
                )
            }
            .map { ($0, intersectionArea($0, frame)) }
            .filter { $0.1 > 0 }
            .max { $0.1 < $1.1 }?
            .0
    }

    private func intersects(_ lhs: CGRect, _ rhs: CGRect) -> Bool {
        intersectionArea(lhs, rhs) > 0
    }

    private func intersectionArea(_ lhs: CGRect, _ rhs: CGRect) -> CGFloat {
        let intersection = lhs.intersection(rhs)
        guard !intersection.isNull, !intersection.isEmpty else {
            return 0
        }

        return intersection.width * intersection.height
    }

    private func cgFloat(_ value: Any?) -> CGFloat? {
        switch value {
        case let value as CGFloat:
            return value
        case let value as Double:
            return CGFloat(value)
        case let value as Int:
            return CGFloat(value)
        case let value as NSNumber:
            return CGFloat(truncating: value)
        default:
            return nil
        }
    }

    private func isStandardWindow(_ window: AXUIElement) -> Bool {
        if axBool(window, kAXMinimizedAttribute as String) == true {
            return false
        }

        return axString(window, kAXSubroleAttribute as String) == kAXStandardWindowSubrole as String
    }

    private func windowFrame(_ window: AXUIElement) -> CGRect? {
        guard
            let origin = axPoint(window, kAXPositionAttribute as String),
            let size = axSize(window, kAXSizeAttribute as String),
            size.width > 0,
            size.height > 0
        else {
            return nil
        }

        return CGRect(origin: origin, size: size)
    }
}

private func axString(_ element: AXUIElement, _ attribute: String) -> String? {
    var value: CFTypeRef?
    guard AXUIElementCopyAttributeValue(element, attribute as CFString, &value) == .success else {
        return nil
    }
    return value as? String
}

private func axBool(_ element: AXUIElement, _ attribute: String) -> Bool? {
    var value: CFTypeRef?
    guard AXUIElementCopyAttributeValue(element, attribute as CFString, &value) == .success else {
        return nil
    }
    return value as? Bool
}

private func axElement(_ element: AXUIElement, _ attribute: String) -> AXUIElement? {
    var value: CFTypeRef?
    guard
        AXUIElementCopyAttributeValue(element, attribute as CFString, &value) == .success,
        let value,
        CFGetTypeID(value) == AXUIElementGetTypeID()
    else {
        return nil
    }
    return (value as! AXUIElement)
}

private func axElements(_ element: AXUIElement, _ attribute: String) -> [AXUIElement]? {
    var value: CFTypeRef?
    guard
        AXUIElementCopyAttributeValue(element, attribute as CFString, &value) == .success,
        let elements = value as? [AXUIElement]
    else {
        return nil
    }
    return elements
}

private func axPoint(_ element: AXUIElement, _ attribute: String) -> CGPoint? {
    guard let value = axValue(element, attribute, expectedType: .cgPoint) else {
        return nil
    }

    var point = CGPoint.zero
    guard AXValueGetValue(value, .cgPoint, &point) else {
        return nil
    }
    return point
}

private func axSize(_ element: AXUIElement, _ attribute: String) -> CGSize? {
    guard let value = axValue(element, attribute, expectedType: .cgSize) else {
        return nil
    }

    var size = CGSize.zero
    guard AXValueGetValue(value, .cgSize, &size) else {
        return nil
    }
    return size
}

private func axValue(_ element: AXUIElement, _ attribute: String, expectedType: AXValueType) -> AXValue? {
    var value: CFTypeRef?
    guard
        AXUIElementCopyAttributeValue(element, attribute as CFString, &value) == .success,
        let value,
        CFGetTypeID(value) == AXValueGetTypeID()
    else {
        return nil
    }

    let axValue = value as! AXValue
    guard AXValueGetType(axValue) == expectedType else {
        return nil
    }
    return axValue
}

private let app = NSApplication.shared
private let delegate = OverlayController()
app.delegate = delegate
app.run()
