//
//  ViewController.swift
//  Insta Caption
//
//  Created by Keyan Fayaz on 2018-02-03.
//  Copyright © 2018 Keyan Fayaz. All rights reserved.
//

import UIKit
import FirebaseCore
import FirebaseDatabase
//import instaFramework

class ViewController: UIViewController, UIImagePickerControllerDelegate, UINavigationControllerDelegate, UIPickerViewDataSource, UIPickerViewDelegate, UITextFieldDelegate {
    
    
    let pickerData = ["Lyrics", "Generic", "Sentimental", "Funny", "Selfie", "Puns", "Motivational"]
    var captions: [String]?
    var imagePass: UIImage?
    
    var dbRef: FIRDatabaseReference {
        return FIRDatabase.database().reference()
    }
    
    override func viewDidLoad() {
        super.viewDidLoad()
        addTapGesture()
        fetchData()
        pickerViewer.dataSource = self
        pickerViewer.delegate = self
    }
    
    override func viewDidAppear(_ animated: Bool) {
        self.view.sendSubview(toBack: background)
        view.bringSubview(toFront: choseImageButtonOutlet)
        view.bringSubview(toFront: generateButton)
        view.bringSubview(toFront: textField)
    }
    
    
    func fetchData() {
        dbRef.child("user1").observe(.childAdded) { (snapshot: FIRDataSnapshot) in
            if let data = snapshot.value as? [String: Any] {
                print(data)
                let urlLoaded = data["image"] as! String
                let url = URL(string: urlLoaded)
                let urlData = try? Data(contentsOf: url!)
                let image = UIImage(data: urlData!)
                self.imagePass = image
                self.imageView.image = image
                self.view.bringSubview(toFront: self.outsideImageVIew)
                self.captions = data["suggested_captions"] as! [String]
                self.textField.text = data["keyword"] as! String
            }
        }
    }
    
    override func prepare(for segue: UIStoryboardSegue, sender: Any?) {
        if let controller = segue.destination as? CaptionViewController {
            controller.cap1 = self.captions![0]
            controller.cap2 = self.captions![1]
            controller.cap3 = self.captions![2]
            controller.imageL = self.imagePass
        }
    }
    
    
    
    func addNewPicture() {
        let picker = UIImagePickerController()
        picker.allowsEditing = true
        picker.delegate = self as UIImagePickerControllerDelegate & UINavigationControllerDelegate
        present(picker, animated: true)
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
    }
    
    func getDocumentsDirectory() -> URL {
        let paths = FileManager.default.urls(for: .documentDirectory, in: .userDomainMask)
        let documentsDirectory = paths[0]
        return documentsDirectory
    }
    
    func imagePickerController(_ picker: UIImagePickerController, didFinishPickingMediaWithInfo info: [String : Any]) {
        guard let image = info[UIImagePickerControllerEditedImage] as? UIImage else {
            print("Errrorrrr")
            return }
        
        let imageName = UUID().uuidString
        let imagePath = getDocumentsDirectory().appendingPathComponent(imageName)
        
        if let jpegData = UIImageJPEGRepresentation(image, 80) {
            try? jpegData.write(to: imagePath)
        }
        
        let data = UIImagePNGRepresentation(image) as Data?
        
        imageView.image = image        
        imageView.isHidden = false
        imageView.isOpaque = true
        view.bringSubview(toFront: outsideImageVIew)
        keywordField.isEnabled = true
        generateButton.isEnabled = true
        choseImageButtonOutlet.isHidden = true
        dismiss(animated: true)
    }

  
    @IBOutlet weak var background: UIImageView!
    @IBOutlet weak var imageView: UIImageView!
    
    @IBAction func chooseImage(_ sender: UIButton) {
        addNewPicture()
    }
    
    @IBAction func generateAction(_ sender: Any) {
    }
    
    @IBOutlet weak var generateButton: UIButton!
    @IBOutlet weak var choseImageButtonOutlet: UIButton!
    @IBOutlet weak var keywordField: UITextField!
    
    @IBOutlet weak var pickerViewer: UIPickerView!
    @IBOutlet weak var textField: UITextField!
    

    @IBOutlet weak var outsideImageVIew: UIView!
    
    //MARK: - Delegates and data sources
    //MARK: Data Sources
    func numberOfComponentsInPickerView(pickerView: UIPickerView) -> Int {
        return 1
    }
    func pickerView(_ pickerView: UIPickerView, numberOfRowsInComponent component: Int) -> Int {
        return pickerData.count
    }
    func pickerView(_ pickerView: UIPickerView, titleForRow row: Int, forComponent component: Int) -> String? {
        return pickerData[row]
    }
    
    func pickerView(_pickerView: UIPickerView, didSelectRow row: Int, inComponent component: Int) {
    }
    func numberOfComponents(in pickerView: UIPickerView) -> Int {
        return 1
    }
    
    func addTapGesture(){
        let tap: UITapGestureRecognizer = UITapGestureRecognizer(target: self, action: #selector(ViewController.dismissKeyboard))
        
        //Uncomment the line below if you want the tap not not interfere and cancel other interactions.
        //tap.cancelsTouchesInView = false
        
        view.addGestureRecognizer(tap)
    }
    
    
    @objc func dismissKeyboard() {
        //Causes the view (or one of its embedded text fields) to resign the first responder status.
        view.endEditing(true)
    }
    
    func alertUser(title: String, message: String, completion: @escaping (UIAlertAction) -> ()) {
        let alert = UIAlertController(title: title, message: message, preferredStyle: .alert)
        let ok = UIAlertAction(title: "Dismiss", style: .default, handler: completion)
        alert.addAction(ok)
        present(alert, animated: true, completion: nil)
    }
    
    
}

