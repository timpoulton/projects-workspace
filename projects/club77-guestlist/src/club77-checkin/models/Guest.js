module.exports = (sequelize, DataTypes) => {
  const Guest = sequelize.define('Guest', {
    id: {
      type: DataTypes.INTEGER,
      primaryKey: true,
      autoIncrement: true
    },
    event_id: {
      type: DataTypes.INTEGER,
      allowNull: false,
      references: {
        model: 'events',
        key: 'id'
      }
    },
    first_name: {
      type: DataTypes.STRING,
      allowNull: false,
      validate: {
        notEmpty: true
      }
    },
    last_name: {
      type: DataTypes.STRING,
      allowNull: false,
      validate: {
        notEmpty: true
      }
    },
    email: {
      type: DataTypes.STRING,
      validate: {
        isEmail: true
      }
    },
    dob: {
      type: DataTypes.DATEONLY
    },
    checked_in: {
      type: DataTypes.BOOLEAN,
      defaultValue: false
    },
    check_in_time: {
      type: DataTypes.DATE,
      allowNull: true
    },
    created_at: {
      type: DataTypes.DATE,
      defaultValue: DataTypes.NOW
    },
    updated_at: {
      type: DataTypes.DATE,
      defaultValue: DataTypes.NOW
    }
  }, {
    tableName: 'guests',
    timestamps: true,
    createdAt: 'created_at',
    updatedAt: 'updated_at'
  });

  Guest.associate = function(models) {
    // Guest belongs to an Event
    Guest.belongsTo(models.Event, {
      foreignKey: 'event_id',
      as: 'event'
    });
  };

  // Instance method to check in a guest
  Guest.prototype.checkIn = async function() {
    this.checked_in = true;
    this.check_in_time = new Date();
    return await this.save();
  };

  // Instance method to check out a guest
  Guest.prototype.checkOut = async function() {
    this.checked_in = false;
    this.check_in_time = null;
    return await this.save();
  };

  return Guest;
}; 