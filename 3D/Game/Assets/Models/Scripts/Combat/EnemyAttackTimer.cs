using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class EnemyAttackTimer : MonoBehaviour {
	protected float timer=0.0f;
	public float invulnerability=1.0f;

	// Use this for initialization
	void Start () {
		//Para que pueda atacar desde el principio
		timer = invulnerability;
	}

	public bool canAttack(){
		if (timer >= invulnerability) {
			timer = .0f;
			return true;
		} else {
			return false;
		}
	}

	// Update is called once per frame
	void Update () {
		timer += Time.deltaTime;
	}
}
