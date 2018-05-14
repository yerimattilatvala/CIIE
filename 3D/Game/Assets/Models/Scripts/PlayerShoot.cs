using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class PlayerShoot : MonoBehaviour {
	private bool block = false;
	[SerializeField]Shooter weapon;

	public void setBlock(bool b){
		block = b;
	}

	void Update() {
		if(block == false)
			if (Input.GetKeyDown(KeyCode.Mouse0))
				weapon.Fire ();
	}
}
