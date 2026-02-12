# src/core/toast.ps1
param (
    [string]$Title,
    [string]$Message
)

$ErrorActionPreference = 'SilentlyContinue'

# Load the Windows Notification Libraries
[Windows.UI.Notifications.ToastNotificationManager, Windows.UI.Notifications, ContentType = WindowsRuntime] > $null
$template = [Windows.UI.Notifications.ToastNotificationManager]::GetTemplateContent([Windows.UI.Notifications.ToastTemplateType]::ToastText02)

# Inject the Title and Message passed from Python
$textNodes = $template.GetElementsByTagName("text")
$textNodes.Item(0).AppendChild($template.CreateTextNode($Title)) > $null
$textNodes.Item(1).AppendChild($template.CreateTextNode($Message)) > $null

# Fire the Toast
$notifier = [Windows.UI.Notifications.ToastNotificationManager]::CreateToastNotifier("xsv Command Center")
$notif = [Windows.UI.Notifications.ToastNotification]::new($template)
$notifier.Show($notif)