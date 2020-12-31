CREATE TRIGGER trigg_to_store AFTER INSERT ON devops.instore FOR EACH ROW
BEGIN
	IF (SELECT id FROM devops.store WHERE project_id = new.project_id AND mtype = new.mtype AND mclass = new.mclass AND mname = new.mname AND specifi = new.specifi ) THEN
			UPDATE devops.store  
			SET num =(SELECT sum( num ) FROM devops.instore WHERE project_id = new.project_id AND mtype = new.mtype AND mclass = new.mclass AND mname = new.mname AND specifi = new.specifi)
		WHERE
			project_id = new.project_id 
			AND mtype = new.mtype 
			AND mclass = new.mclass 
			AND mname = new.mname 
			AND specifi = new.specifi;
	ELSE 
		INSERT INTO devops.store SET project_id = new.project_id,
			mtype = new.mtype,
			mclass = new.mclass,
			mname = new.mname,
			specifi = new.specifi,
			num =(SELECT sum( num ) FROM devops.instore WHERE project_id = new.project_id AND mtype = new.mtype AND mclass = new.mclass AND mname = new.mname AND specifi = new.specifi),
			unit = new.unit;
	END IF;
END 





CREATE TRIGGER trigg_out_store AFTER INSERT ON devops.outstore FOR EACH ROW
BEGIN
	UPDATE devops.store 
		SET num = (SELECT tmp.num from (SELECT num FROM devops.store WHERE id = new.store_id) tmp) - new.num 
	WHERE
		id = new.store_id;
END 