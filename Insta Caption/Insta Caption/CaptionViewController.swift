//
//  CaptionViewController.swift
//  Insta Caption
//
//  Created by Francesco Virga on 2018-02-04.
//  Copyright © 2018 Keyan Fayaz. All rights reserved.
//

import UIKit

class CaptionViewController: UIViewController {

    @IBOutlet weak var caption1: UILabel!
    
    @IBOutlet weak var caption2: UILabel!
    
    @IBOutlet weak var caption3: UILabel!
    
    var cap1: String?
    var cap2: String?
    var cap3: String?
    var imageL: UIImage?
    
    @IBOutlet weak var imageLoad: UIImageView!
    override func viewDidLoad() {
        super.viewDidLoad()
        initializeCaptions()
        // Do any additional setup after loading the view.
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }
    
    func initializeCaptions() {
        if cap1 != nil {
            caption1.text = cap1
            caption2.text = cap2
            caption3.text = cap3
            imageLoad.image = imageL
        }
        else {
            caption1.text = "What do you think of the view?"
            caption2.text = "Keep smiling because life is a beautiful thing and there’s so much to smile about."
            caption3.text = "Girls just wanna have sun"
        }
    }
    
    @IBAction func happyReaction(_ sender: Any) {
        alertUser(title: "Enjoy the ❤️", message: "Hope to see you again soon!")
    }

    @IBAction func sadReaction(_ sender: Any) {
        alertUser(title: "Sorry about that!", message: "We will consider this and improve our system for next time 😘")
    }
    
    func alertUser(title: String, message: String) {
        let alert = UIAlertController(title: title, message: message, preferredStyle: .alert)
        let ok = UIAlertAction(title: "Dismiss", style: .default, handler: nil)
        alert.addAction(ok)
        present(alert, animated: true, completion: nil)
    }

}
